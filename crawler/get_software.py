# -*- encoding:utf-8 -*-

import os
import re
import requests
from bs4 import BeautifulSoup

def get_url():
	url = 'http://en.wikipedia.org/wiki/List_of_RNA_structure_prediction_software'
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	result = soup.find_all('a', text=['webserver', 'sourcecode', 'link', 'executables', 'NUPACK', 'linuxbinary'])
	print len(result)
	hrefs = set()
	for item in result:
		print item['href']
		hrefs.add(item['href'])
	fp = open('hrefs.txt', 'w')
	for item in hrefs:
		fp.write(item + '\n\n\n')
	fp.close()

if __name__ == '__main__':
	os.system('printf "\033c"')

	get_url()
