#!/usr/bin/env python
#coding=utf-8
import  requests
def test():
	headers = {'apikey':'9602ab6a150f90297cabae56d6013e93'}
	r = requests.get('http://apis.baidu.com/apistore/stockservice/hkstock?stockid=00168&list=1', headers = headers)
	print r.encoding
	result = r.text.decode("unicode_escape").encode("utf-8")	
	print  (result)
test()