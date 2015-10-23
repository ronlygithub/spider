#coding=utf-8
import urllib2
import re
import StringIO, gzip

def getHtml(url):
    page = urllib2.urlopen(url) 
    # get the html from given url
    html = page.read()    
    # if this page is compressed by gzip then decomression first
    if( page.info().get('Content-Encoding')  == 'gzip'):
    	html = StringIO.StringIO(html)
    	html =  gzip.GzipFile(fileobj=html)
    write("soufang.txt",html)
    return html

def getDetailPageUrl(html):
     # get house list part in html 
     html = read("soufang.txt")
     divReg = re.compile(r'shaixuan[\s\S]*?divMaylikeUl')
     divHouseList = divReg.findall( str(html))
     
     # pattern for housedetail page url
     reg  = r'http://\w+?\.fang\.com/(?=")'
     detailUrlReg = re.compile(reg)
     detailList = detailUrlReg.findall(divHouseList[0])
     detailList = list(set(detailList))
     detailList = [line+'\n' for line in detailList]
     print len(detailList)
     write("souFangDetailPageUrls.txt",detailList)
     

def write(path,html):
     print 'write start'
     f = file(path,"a")
     f.writelines(html)
     f.close()	
     print 'write completed'

def read(path):
     print 'reading'
     input  = open(path, "r")
     html = input.read()	
     input.close()
     return html


html = getHtml("http://newhouse.sy.fang.com/house/s/")
getDetailPageUrl(html)

def main():
     startURL = "http://newhouse.sy.fang.com/house/s/"
     


