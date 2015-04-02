#-*- coding:utf-8 -*-
#!/usr/bin/env python

import requests
import os
from bs4 import BeautifulSoup
import bs4
from Queue import Queue
import threading
import time
from types import NoneType

class QiuShiBaiKe:#(threading.Thread):
	def __init__(self, url, num):
		self.url = url
		self.num = num

	def get_html(self):
		global share_data
		response = requests.get(self.url)
		#share_data.put(response.text)
		share_data.append(response.text)

class ParseBaike:
	def __init__(self, start_page):
		self.start_page = start_page 
	def get(self):
		#start = start_page
		while True:
			if len(share_data) > 0:
				print 'page', self.start_page, 'start'
				content = share_data.pop(0)
				soup = BeautifulSoup(content)
				div_content = soup.find_all('div', class_='content')
				comment = soup.find_all('span', class_='stats-vote')
				for i in xrange(len(div_content)):
					if type(div_content[i].string) == NoneType:
						for item in div_content[i]:
							if type(item) == bs4.element.Tag:
								pass
							else:
								print item.strip()
					else: 
						print div_content[i].string.strip()
					raw_input()
				print 'page', self.start_page, 'end'
				self.start_page += 1
			else:
				break

share_data = [] 
def main():
	url_base = 'http://www.qiushibaike.com/hot/page/'
	start_page = raw_input('please enter start page: ')
	end_page = raw_input('please enter end page: ')
	for i in xrange(int(start_page), int(end_page)):
		#print 'page: ', i
		url = url_base + str(i)
		qiushibaike = QiuShiBaiKe(url, i)
		qiushibaike.get_html()
	#pages = range(int(start_page), int(end_page))
	parsebaike = ParseBaike(int(start_page))
	parsebaike.get()

if __name__ == '__main__':
	os.system('printf "\033c"')

	main()
