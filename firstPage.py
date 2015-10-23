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
    return html

def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    x = 0
    for imgurl in imglist:
        urllib2.urlretrieve(imgurl,'/home/ronly/%s.jpg' %x)
        x+=1

def write(html):
     print 'write start'
     f = file("soufang.txt","w+")
     f.writelines(html)
     f.close()	
     print 'write completed'


html = getHtml("http://newhouse.sy.fang.com/house/s/")
write(html)

