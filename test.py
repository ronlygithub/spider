#!/usr/bin/env python
#coding:utf-8
from bs4 import BeautifulSoup 
import urllib
import re 

"""
结构分析

      
">
         
">
        
">
        

          
://www.cnpythoner.com/" rel="nofollow">首页

://www.cnpythoner.com/catalog.asp?cate=11">入门教程

://www.cnpythoner.com/catalog.asp?cate=4">练习题

://www.cnpythoner.com/catalog.asp?cate=1">python教程

://www.cnpythoner.com/catalog.asp?cate=2">django教程

://www.cnpythoner.com/catalog.asp?cate=15">seo应用

://www.cnpythoner.com/catalog.asp?cate=16">linux

://www.cnpythoner.com/catalog.asp?cate=17">测试应用

://www.cnpythoner.com/pythonbook.html" target="_blank">书籍推荐

://www.cnpythoner.com/pythondown/pythondown.html" target="_blank">环境下载
"""

def url_info(url):
    page = urllib.urlopen(url) 
    soup = BeautifulSoup(page)
    tag=soup.find_all('div',{'id':'divNavBar'})
    #print list 
    for i in tag:
        #print i.find_all('li')
        url_list=i.find_all('li')
        for j in url_list:
            #print j
            print j.a['href']
       
if __name__=="__main__": 
     url_info('http://www.cnpythoner.com')