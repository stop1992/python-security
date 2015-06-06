
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
import time


if __name__ == '__main__':
	os.system('printf "\033c"')
	
	# start = time.clock()
	start = time.time()
	# for i in xrange(10000):
	try:
		response = requests.get('http://guba.eastmoney.com/list,000002,f_1.html')
		pattern = re.compile(ur'共有帖子数 (\d+) 篇')
		result  = pattern.search(response.text)
		# print type(result)
		num = int(result.group(1))
		print num, type(num)
	except Exception, e:
			print str(e)
		# print 'get error'
