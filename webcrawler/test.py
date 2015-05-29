# -*- encoding: utf-8 -*-

import os
# import Queue
# import threading
# import Queue
import re
import requests
from bs4 import BeautifulSoup
import codecs
from selenium import webdriver

class Zhihu(object):
	def __init__(self, url):
		self.url = url

	def handle(self):
		login_url = 'http://www.zhihu.com/login'
		post_data = {
			'email':'1447932441@qq.com',
			'password':'zhihuZHIHU68'
			}
		session = requests.session()
		# login_response = requests.post(login_url, data=post_data)
		login_response = session.post(login_url, data=post_data)
		print login_response.text
		# fp = codecs.open('tmp.txt', mode='w', encoding='utf-8')
		# fp.write(login_response.text)
		# fp.close()

		# raw_input('press any key to continue')
		# _cookies = login_response.cookies
		
		# response = requests.get(self.url, cookies=_cookies)
		response = session.get(self.url)
		# fp = codecs.open('tmp2.txt', mode='w', encoding='utf-8')
		# fp.write(response.text)
		# fp.close()
		soup = BeautifulSoup(response.text)
		# attrs = {
				# 'class_':'time',
				# 'data-timestamp':r'\d+'
				# }
		# asktime = soup.find_all(attrs=attrs)
		# asktime = soup.find_all(class_='time', data-timestamp=r'\d+')#re.compile(r'\d+'))
		# asktime = soup.find_all('span', class_='time')
		# <a class="zg-link-gray-normal meta-item" target="_blank" href="/question/29115861">4 个回答</a>
		# yesnum = soup.find_all('a', class_='zg-link-gray-normal meta-item')
		# yesnum = soup.find_all('a', href=re.compile(r'/question/\d+'), target="_blank")
		# yesnum = soup.find_all('a', class_=re.compile(r'zg\-link\-gray\-normal meta\-item'))
		yesnum = soup.find_all('a', class_=re.compile(r'zg\-link\-gray\-normal'))
		# yesnum = soup.find_all('a')
		# for item in asktime:
			# print item.string
		for item in yesnum:
			print item.string
			# print item.string
			# print type(item)
		# print len(asktime)
		print len(yesnum)
		
if __name__ == '__main__':
	os.system('printf "\033c"')

	url = 'http://www.zhihu.com/topic/19776749/questions?page=1'
	zhihu = Zhihu(url)
	zhihu.handle()

