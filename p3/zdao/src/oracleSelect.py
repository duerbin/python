#########################################################################
# -*- coding: utf-8 -*-
#File Name: oracleSelect.py
# Author: dueb
# mail: duerbin@126.com
# Created Time: 2014年03月11日 星期二 14时55分31秒
#########################################################################
#!/usr/bin/env python
import threading
import Queue
import urlparse
import requests
import cookielib
import urllib2
import urllib
import re
import time
from bs4 import BeautifulSoup

class zaScrapy(object):
	def __init__(self,url):
		self.url=url
		self.cookie_filename='cookie.txt'

	def GetAppID(self):		
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Connection':'keep-alive'
		}

		req = urllib2.Request(url,headers=headers)
		cookie=cookielib.MozillaCookieJar(self.cookie_filename)
		handler=urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(handler)
		response = opener.open(req)
		cookie.save(ignore_discard=True, ignore_expires=True)
		#print response.read()
		#pattern=re.compile(r'log_config.*}')
		#log_config=re.search(pattern,response.read()).group()
		#strlist=log_config.split('\"')
		#return strlist[3]
		soup=BeautifulSoup(response.read())
		all_tags=soup.findAll('input',{'id':'csrf_token'})
		for tags in all_tags:
			appid= tags['value']
		self.appid=appid
	
	def LogApp(self,loginurl,username,passwd):
		print "LogApp"
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Accept':'application/json, text/javascript, */*; q=0.01',
			'Referer':'https://www.zdao.com/user/login?redirect=https%3A%2F%2Fwww.zdao.com%2F',
			'Connection':'keep-alive',
			'Host': 'www.zdao.com',
			'Accept-Encoding': 'gzip, deflate, br',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'X-Requested-With': 'XMLHttpRequest'
		}
		cookie = cookielib.MozillaCookieJar()
		cookie.load(self.cookie_filename, ignore_discard=True, ignore_expires=True)
        		
		#self.appid='test'
		value={'YII_CSRF_TOKEN':self.appid,'account':username,'password':passwd,'keep_login':1}
		time.sleep(5)
		print value
		data=urllib.urlencode(value)
		print data
		req=urllib2.Request(loginurl,data,headers)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		response = opener.open(req)		
		cookie.save(ignore_discard=True, ignore_expires=True)
		print response.read()

	def GetUserInfo(self,reUrl):
		print "a"
		reUrl="https://www.zdao.com/message/sysmsglist"
		print "GetUserInfo"
		cookie = cookielib.MozillaCookieJar()
		cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
		req = urllib2.Request(url)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		response = opener.open(req)
		print response.read()


if __name__=="__main__":
	url="https://www.zdao.com"
	loginurl="https://www.zdao.com/user/ajaxlogin"
	zdtest=zaScrapy(url)
	zdtest.GetAppID()
	zdtest.LogApp(loginurl,'18515156558','123456')
	time.sleep(5)
	#zdtest.GetUserInfo("test")