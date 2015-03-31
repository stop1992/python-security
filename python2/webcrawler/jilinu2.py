#-*-coding:utf-8-*-
#!/usr/bin/env python

import urllib2
import os
import cookielib
import urllib
import re
import types
import time
import requests

import mythread

class JiLinU:
	def __init__(self, urls, data):
		self.urls = urls
		self.data = data
	def get_data(self):
		session = requests.Session()
		response = session.post(self.urls[0], data=self.data)
		score = session.get(self.urls[1])

def get_urls():
	urls = []
	urls.append('http://gim.jlu.edu.cn/check.jsp')
	urls.append('http://gim.jlu.edu.cn/pyc/menu_stu.jsp?menu=xuanke_check')
	return urls

if __name__ == '__main__':
	os.system('printf "\033c"')

	data = {'username':'2014544007', 'password':'709860'}
	urls = get_urls()
	jilinu = JiLinU(urls, data)
