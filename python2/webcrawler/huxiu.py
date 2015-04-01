#-*- conding:utf-8 -*-
#!/usr/bin/env python

from bs4 import BeautifulSoup
import os
import requests

class HuXiu:
	def __init__(self, url):
		self.url = url

	def get_data(self):
		self.html_data = requests.get(self.url)
		self.html_data.encoding = 'utf-8'

	def extract_data(self):
		soup = BeautifulSoup(self.html_data.text)
		a_class_tittle = soup.find_all(class_='title')
		div_class_title = soup.find_all(class_=['mob-sub', 'mod-summary'])
		for i in range(len(a_class_tittle) - 1):
			print a_class_tittle[i].string
			print '    ' + div_class_title[i].string

if __name__ == '__main__':
	os.system('printf "\033c"')

	url = 'http://www.huxiu.com/'
	huxiu = HuXiu(url)
	huxiu.get_data()
	huxiu.extract_data()
