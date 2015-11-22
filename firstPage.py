#coding=utf-8
import urllib2
import re
import StringIO, gzip
from bs4 import BeautifulSoup

def storeHtml():
      for  pageIndex in range(1,222):
              print 'processing  %d page' %pageIndex
              url = 'http://newhouse.sy.fang.com/house/s/b9{0}'.format(pageIndex)       
              html = getHtml(url)
              write('./html/sySoufangPage_%d.txt' %(pageIndex),'w',html)
              print 'page %d completed' %pageIndex

def getHtml(url):
    try:
        page = urllib2.urlopen(url,timeout = 20) 
        # get the html from given url
        html = page.read()    
        # if this page is compressed by gzip then decomression first
        if( page.info().get('Content-Encoding')  == 'gzip'):
        	html = StringIO.StringIO(html)
        	html =  gzip.GzipFile(fileobj=html)    
        return html
    except:
        print "get content from  %s error" %url

def getDetailPageUrl(html):
     # prser html with BeautifulSoup
     soup = BeautifulSoup(html,"html5lib")
     # get the div from html  where its class equals to nl_con
     divHouseList = soup.find_all('div',class_="nl_con")   
     # pattern for housedetail page url
     # reg  = r'http://\w+?\.fang\.com/\d*?/?(?=")'
     reg  = r'http://\w+?\.fang\.com/\d*?/?(?=")|http://\w+?\.fang\.com/shop/(?=")|http://\w+?\.fang\.com/office/(?=")' 
     detailUrlReg = re.compile(reg)
     detailList = detailUrlReg.findall(str(divHouseList))
     detailList = list(set(detailList))
     detailList = [line+'\n' for line in detailList]
     return detailList   

def getDetailPageUrlList():
        detailPageUrls = []
        for index in range(1,222):
            file = './html/sySoufangPage_{0}.txt'.format(index)
            html = read(file)           
            urls = getDetailPageUrl(html)  
            print './html/sySoufangPage_%d.txt              urlNumbers: %d' %(index,len(urls)       )
            if len(detailPageUrls) !=0:
            	 detailPageUrls.extend(urls)
            else:
               detailPageUrls = urls
        print len(detailPageUrls)
        write('./html/sySoufangDetailPageUrl.txt', 'w',detailPageUrls)

def write(path,model,html):
     f = file(path,model)
     f.writelines(html)
     f.close()	

def read(path):
     input  = open(path, "r")
     html = input.read()	
     input.close()
     return html

def storeDetailPageHtml():
     detailPageUrls  = read("./html/sySoufangDetailPageUrl.txt")
     index = 1
     for url in detailPageUrls.split("\n"):
     	if url == '' :
     		continue
     	detailPage = getHtml(url)
     	fileName = "./detailPage/{0}.txt".format(index)
     	print "processing %s from %s" %(fileName ,url)
     	if not detailPage:
     		continue
     	write(fileName,"w",detailPage)
     	index +=1

       
     # storeDetailPageHtml()
     # getHtml("sfsdfd")
     # getDetailPageUrlList()
def getHouseInfo(html,file):
	houseInfo = []
	soup = BeautifulSoup(html,"html5lib")
	try:
		divInformation = soup.find_all('div',class_= 'information_li')
		if len(divInformation) == 0:
			print 'can not find class information_li in %s  ' %file
			return houseInfo
		houseInfo.append(getHouseInfoTitle(soup))
		houseInfo.append(getHouseInfoPrice(divInformation))
		scorecontent = divInformation[2].find('a',attrs={'id':'scoretotalcontent'})
		# houseInfo['score'] = getHouseInfoScore(scorecontent)
		# houseInfo['comment'] = getHouseInfoComment(scorecontent)
		houseInfo.append(getHouseInfoAddress(divInformation))
		houseInfo.append(getHouseInfoDetail(divInformation))
		return houseInfo
	except Exception, e:
		print 'get house information from %s error' %file
		print e

def getHouseInfoDetail(divInformation):
	a = divInformation[6].a
	return a['href']

def getHouseInfoAddress(divInformation):
	address = divInformation[4].p.span
	return address['title'].encode('utf-8')

def getHouseInfoComment(scorecontent):
	try:
		spans = scorecontent[0].find_all('span')
		return spans[1].text
	except Exception, e:
		print 'get comment error'
		print e
	
def getHouseInfoTitle(soup):
	divDaohang = soup.find_all('div',attrs={'id':'daohang'})    
	try:
		a = divDaohang[0].a
		return  a['title'].encode('utf-8')
	except Exception, e:
		print 'get title error'
		print e
		return ' '

def getHouseInfoPrice(divInformation):
	try:	
		span =  divInformation[0].span
		return span.text
	except Exception, e:
		print 'get price error'
		print e	
		return ' '

def getHouseInfoScore(scorecontent):
	try:
		score =  scorecontent[0].span
		return score.text
	except Exception, e:
		print 'get score error'
		print e	
		return ' '

def storeHouseInfo(start,end):
        detailPageUrls = []
        for index in range(start,end):
            file = './detailPage/{0}.txt'.format(index)
            html = read(file)
            houseInfo = getHouseInfo(html,file)  
            if not houseInfo:
            	 write('errorInfo.txt','a',file+'\t')
            	 continue
            if len(houseInfo) ==0:
            	 write('errorInfo.txt','a',file+'\t')
            	 continue
            houseInfo = [line+'\t' for line in houseInfo]
            houseInfo.append('\n')
            try:
	          write("./houseInfos.txt",'a',houseInfo)
	          print 'file %s  writed' %file	      
            except Exception, e:
	            print e
                    

storeHouseInfo(703,704)
