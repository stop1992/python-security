# -*- coding:utf-8 -*-

import os
#import requests
#from bs4 import BeautifulSoup
#import re
from selenium import webdriver

class GetProxyIP:
	def __init__(self, url):
		"""
			url:string
		"""
		self.url = url 

	def get_data(self):
		driver = webdriver.PhantomJS()
		driver.get(self.url)
		trs = driver.find_elements_by_tag_name('tr')

		fp = open('proxyip.txt', 'w')
		for i in xrange(1, 51):
			# get each tr data
			line_data = trs[i].text.split()
			if line_data[len(line_data)-2] == u'空闲':
				fp.write(line_data[1]+':'+line_data[2]+'\n')
		fp.close()

if __name__ == '__main__':
	os.system('printf "\033c"')
	
	#url = "http://pachong.org/area/short/name/cn/type/high.html"
	url = 'http://pachong.org/'
	proxyip = GetProxyIP(url)
	proxyip.get_data()
