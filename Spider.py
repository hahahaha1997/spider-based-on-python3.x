import urllib.request
import urllib.error
import time
import re
import pyExcelerator

ind = 2
num = 1

def getHtml(url):
        try:
        #url in these function has checked
            req = urllib.request.Request(url,headers=headers)
            page = urllib.request.urlopen(req,timeout=500)
            html = page.read()
        except ConnectionResetError:
            time.sleep(1)
            getHtml(url)
        return html

def getUrls(html):

    try:
        html = html.decode("utf-8",'ignore')
    finally:
        return None
    pattern = re.compile(r"<a href=\"https?.*?\"")
    urls = pattern.findall(html)# 匹配模式为忽略大小写

    return urls

def oper_on_urls(urls):
    for url in range(len(urls)):
        url_untest = urls[url]  # url in this time with a format"http[s]://url[/]"

        # delete the "/"in the url to make comparision easily
        url_untest.rstrip()
        if url_untest[len(url_untest) -2 ] == "/":
            urls[url] = url_untest[ 9: len(url_untest) - 2]
        else:
            urls[url] = url_untest[ 9 : len(url_untest) - 1]


# find 500 urls
def findpage(pages,ind,num):

    if len(pages) == 0:
        return
    for item in range(len(pages)):

        html = getHtml(pages[item])
        urls = getUrls(html)  # urls in this time with a format"<a href="http[s]://url[/]"

        if len(urls) == 0:#if the url set is empty,them manage the next urls set
            continue
        oper_on_urls(urls)  # urls in this time with a format"http[s]://url"

        for url in urls:
            try:
                req = urllib.request.Request(url,headers=headers)
                pa = urllib.request.urlopen(req)
                ht = pa.read()
            except:
                continue
            if pa.getcode() == 200:  # the url is accessible

                if url in dictionary :
                    continue
                else:# no exist in the dictionary

                    dictionary[url]=ind
                    html_list.append(ht)
                    pages_to_next.append(url)
                    ind += 1
                    num += 1
                    print(num)
                    if num == 500 :
                        return


    pages.clear()
    pages=pages_to_next.copy()
    pages_to_next.clear()

    findpage(pages,ind,num)

def search_B_in_A(html,url_B):

    if (html.find(url_B))!= -1:
        return False
    else:
        return True

def rev(ss):
    string = ss.split('.')
    string.reverse()
    return ".".join(string)

#data define
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
index = 2
number = 1  #the index to the dictionary,num is a variable to be a loop controled variable
matrix = [([0] * 500) for i in range(500)]
matrix2 = [([0] * 500) for i in range(500)]

dictionary = {'http://www.mit.edu/':1}#dictionary to store the url and their index
pages = ["http://www.mit.edu/"]
pages_to_next=[]
key_list=[]
html_list=[]
#operation

html_list.append(getHtml(pages[0]))
findpage(pages,index,number)

dicfile = open('dic.txt','w')

for key in dictionary:
    print((key,dictionary[key]), file=dicfile)
dicfile.close()

for url_A in dictionary:#the matrix is unorder
    html = html_list[dictionary[url_A]-1]
    try:
        html = html.decode('utf-8','ignore')
    except:
        continue
    finally:
        html = None
    for url_B in dictionary:
        if search_B_in_A(html,url_B) == True:
            matrix[dictionary[url_A]-1][dictionary[url_B]-1] = 1

dicfile = open('matrix.txt','w')
for i in matrix:
    for j in i:
        print(" %d "%j,file=dicfile)
dicfile.close()

key_list=list(dictionary.keys())
for item in range(len(key_list)):
    key_list[item] = rev(key_list[item])#inverted the urls

key_list.sort()

for row in range(500):#the matrix2 is ordered,
    for col in range(500):
        matrix2[row][col] = matrix[dictionary[(rev(key_list[row]))]-1][dictionary[(rev(key_list[col]))]-1]
for row_col in range(500):#set the domainant line is 0
    matrix2[row_col][row_col] = 0

dicfile = open('matrix_inorder.txt','w')
for i in matrix2:
    for j in i:
        print(" %d "%j,file=dicfile)
dicfile.close()