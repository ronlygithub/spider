#!/usr/bin/env python
#coding=utf-8
import requests
import re
import os
import StringIO, gzip
import sys
from bs4 import BeautifulSoup
import threading,time
from time import ctime,sleep
	
def now() :
	return str( time.strftime( '%Y-%m-%d %H:%M:%S' , time.localtime() ) )

class syfcSummary():
	# def __init__(self,fileName):
	# 	super(syfcSummary,self).__init__()
	# 	self.fileName = fileName
	# def run(self):
	# 	print self.fileName
	# 	self.getDoorList(self.fileName)
	def write(self,path,model,html):
     		f = file(path,model)
     		f.writelines(html)
    		f.close()	

	def read(self,path):
	     input  = open(path, "r")
	     html = input.readlines()	
	     input.close()
	     return html


	def downloadProjectsInfo(self,start,end):		
		for index in xrange(start,end):
			url = 'http://www.syfc.com.cn/work/xjlp/new_buildingcx.jsp?page={0}'.format(index)
			try:
				print 'downloading  page: %d '  %(index)
				print url
				page = requests.get(url,timeout=20)
				self.getProjectsList(page.content)
       				self.write('./syfcSummary/syfcSummary_{0}.txt'.format(index),'w',page.content)
			except Exception, e:
				print e       	
       	def getProjectsList(self,page):       		  		
		try:	
			print "processing page"
			soup = BeautifulSoup(page, 'html5lib')
			projects = soup		
			pageReg = re.compile('<!-- 新建楼盘列表开始[\s\S]*')
			tmp = pageReg.findall(str(projects))
			soup = BeautifulSoup("".join(tmp),'lxml')

			projectsList =  soup.find_all('table')[0].find_all('tr')
			self.getProjectsInfo(projectsList)			
		except Exception, e:
			print e

       	def getProjectsInfo(self,projectsList):
       		print "processing project"
       		count = 0
       		for project  in projectsList:
			infos = project.find_all("td")  
			# print infos	
			if len(infos) <6:
					continue	
			if count == 0:
				count = count+1
				continue
			try:
				count = count+1
				herf = infos[0].a['href']+'\t'
				projectName = infos[0].a.text.strip()+'\t'
				area = infos[1].text.strip()+'\t'
				compony = infos[3].text.strip()+'\t'
				openTime = infos[4]. text+'\t'
				componyLocation = infos[5].text.strip()+'\r'
				result =  herf+projectName+area+openTime+compony+componyLocation
				self.write("./projectList.txt",'a',result)
			
				# print result
			except Exception, e:
				print "error while processing %s"  %(str(project))
		print count

	def getBuildingsHtml(self):
		     projectsList = "".join(self.read("./projectList.txt")).split("\r")
		     url = "http://www.syfc.com.cn"
		     fileNameReg = re.compile("xmmcid.*$")
		     reg = re.compile("楼盘信息[\s\S]*脚标")
		     count = 1
		     for project  in projectsList:
		     		try:
		     			if len(project) <=0:
		     				continue
					herf = url+ project.split("\t")[0]
					print herf
					buildingInfos = self.downloadingHtml(herf)
					soup = BeautifulSoup(buildingInfos.content,'html5lib')
					
					infos = reg.findall(str(soup))
					# print infos
					fileName = fileNameReg.findall(herf)[0].replace("/"," ")
					self.write("./syfcProjectInfo/project_{0}".format(fileName),"w",infos)
					print fileName
		     		except Exception, e:
		     			print  e
		     		
	def downloadingHtml(self,url):
		print 'downloadingHtml from %s' %(url)
		page = requests.get(url,timeout=20)
		return page
	def getHouseList(self):
		fileList = os.listdir("./syfcProjectInfo")
		fileNameReg = re.compile("(?<=xmmcid=)[\d]+")
		for fileName in fileList:
			# fileName = 'project_xmmcid=402&xmmc=金地盛世'
			print "processing fill %s" %(fileName)
			projectID =  fileNameReg.findall(fileName)[0]
			html = self.read("./syfcProjectInfo/"+fileName)
			reg = re.compile('纳入网上销售总套数[\s\S]*(?=height=\"35\")')
			html = reg.findall("".join(html))
			soup = BeautifulSoup("".join(html),'lxml')
			houseList =  soup.find_all("tr")
			print len(houseList)
			for  house in houseList:
				# print house
				self.getHouseInfo(house,projectID)
		
		# print houseList
	def getHouseInfo(self, house,projectID):
		try:
			houseInfo = house.find_all('td')
			if len(houseInfo) != 5 :
				return
			herf = houseInfo[0].a['href']
			houseLocation = houseInfo[0].a.text
			selling = houseInfo[1].text
			disabledSell = houseInfo[2].text
			selled = houseInfo[3].text
			total = houseInfo[4].text
			reg = re.compile('(?<=houseid=)[\s\S]+?(?=&)')
			houseID = reg.findall(herf)[0]
			result  = [houseID, projectID,herf,houseLocation,selling,disabledSell,selled,total]
			result = "\t".join(result)+"\r"
			# print result
			self.write("./houseList.txt",'a',result)
		except Exception, e:
			print e
			self.write("./houseList.error",'a',house) 

	def getDoorList(self,fileName):
		urlpref = "http://www.syfc.com.cn"
		houseList = "".join(self.read(fileName)).split("\r")
		doorReg = re.compile('<iframe[\s\S]+?</iframe>')
		doorsListUrlReg = re.compile('(?<=src=\")http://www.syfc[\s\S]+?(?=\")')
		for house in houseList:
			try:
				houseInfos = house.split("\t")
				print len(houseInfos)
				if len(houseInfos) !=8:
					continue
				houseInfos = house.split("\t")
				if houseInfos[-1] == 0:
					continue
				url = urlpref+houseInfos[2]
				housePage = self.downloadingHtml(url)				
				iframe = doorReg.findall(housePage.content)
				doorsListUrl = doorsListUrlReg.findall("".join(iframe))[0]
				doorListPage = self.downloadingHtml(doorsListUrl)
				soup = BeautifulSoup(doorListPage.content,'lxml')
				doorsList =  soup.find_all('a')
				self.getDoorsInfo(doorsList,houseInfos[0],houseInfos[1])	
			except Exception, e:
				print e
				self.write('./doorsList.error','a',url+"\r")			
		
	
	def getDoorsInfo(self,doorsList,houseID,projectID):
		urlpref = "http://www.syfc.com.cn"
		sxztReg = re.compile('(?<=xszt=)[\s\S]+$')
		doorIDReg = re.compile('(?<=id=)[\s\S]+?(?=&)')
		doorUrl = urlpref
		doorsOfHouse = []
		for door in doorsList:
			try:
				doorUrl = urlpref+door['href']
				doorPage = self.downloadingHtml(doorUrl)
				# doorPage = doorReg.findall(doorPage)
				soup = BeautifulSoup(doorPage.content,'html5lib')
				contents = soup.find_all('td',class_='font_lan',attrs={'bgcolor':True})				
				doorID = doorIDReg.findall(doorUrl)[0]
				doorInfo = [doorID,houseID,projectID]
				del contents[-1]
				for content in contents:
					doorInfo.append(content.text.strip())
				xszt = sxztReg.findall(door['href'])[0]
				doorInfo.append(xszt)
				doorsOfHouse.append("\t".join(doorInfo))
			except Exception, e:
				print e
				self.write('./doorsInfo.error','a',doorUrl+"\r")
		if len(doorsOfHouse) > 0:
			self.write('./doorsInfo/{0}'.format(projectID),'a',"\r".join(doorsOfHouse)+"\r")

		
		

def threads():
	threadPool = []
	print 'starting at', now()
	for x in xrange(1,7):
		fileName = "./data/houseList.txt.{0}".format(x)
		threadPool.append(syfcSummary(fileName))
	for th in threadPool:
		th.start()
	for th in threadPool:
		th.join()
	print 'all done at: ', now()
	
		
reload(sys)
sys.setdefaultencoding('utf-8')
summary = syfcSummary()
# summary.downloadProjectsInfo(1,109)
# summary.getBuildingsHtml()
# summary.getHouseList()
summary.getDoorList('./data/houseList.txt')
# threads()

