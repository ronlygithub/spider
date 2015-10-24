#coding=utf-8
import urllib2
import re
import StringIO, gzip
from bs4 import BeautifulSoup

def getHtml(url):
    page = urllib2.urlopen(url) 
    # get the html from given url
    html = page.read()    
    # if this page is compressed by gzip then decomression first
    if( page.info().get('Content-Encoding')  == 'gzip'):
    	html = StringIO.StringIO(html)
    	html =  gzip.GzipFile(fileobj=html)    
    return html

def getDetailPageUrl(html):
     # prser html with BeautifulSoup
     soup = BeautifulSoup(html,"html5lib")
     # get the div from html  where its class equals to nl_con
     divHouseList = soup.find_all('div',class_="nl_con")   
     # pattern for housedetail page url
     reg  = r'http://\w+?\.fang\.com/\d*?/?(?=")'
     detailUrlReg = re.compile(reg)
     detailList = detailUrlReg.findall(str(divHouseList))
     detailList = list(set(detailList))
     detailList = [line+'\n' for line in detailList]
     return detailList   

def write(path,model,html):
     print 'write start'
     f = file(path,model)
     f.writelines(html)
     f.close()	
     print 'write completed'

def read(path):
     input  = open(path, "r")
     html = input.read()	
     input.close()
     print html
     return html

# getDetailPageUrl(html)

def storeHtml():
      for  pageIndex in range(1,222):
              print 'processing  %d page' %pageIndex
              url = 'http://newhouse.sy.fang.com/house/s/b9{0}'.format(pageIndex)       
              html = getHtml(url)
              write('./html/sySoufangPage_%d.txt' %(pageIndex),'w',html)
              print 'page %d completed' %pageIndex

def getDetailPageUrlList():
        detailPageUrls = []
        for index in range(1,222):
            file = './html/sySoufangPage_{0}.txt'.format(index)
            html = read(file)           
            urls = getDetailPageUrl(html)  
            print './html/sySoufangPage_%d.txt              urlNumbers: %d' %(index,len(urls)       )
            if not detailPageUrls:
                detailPageUrls = urls
            else:
                detailPageUrls.extend(urls)
        print len(detailPageUrls)
        write('./html/sySoufangDetailPageUrl.txt', 'w',detailPageUrls)

def main():        
    getDetailPageUrlList()
       
main()
