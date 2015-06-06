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
	
	# os.system('scrapy shell http://guba.eastmoney.com/list,000002,f_1.html')

	# print response.url
	fp = codecs.open('text.txt', mode='r', encoding='utf-8')
	data = fp.readlines()
	print len(data)
	# tmp_data= unicode(data)
	tmp_data = ','.join(data)
	pattern = re.compile(ur'共有帖子数 (\d+) 篇')
	# pattern = re.compile(ur'共有')
	result = pattern.findall(tmp_data)
	print result
	# start = time.clock()
	# start = time.time()
	# for i in xrange(10000):
		# try:
			# response = requests.get('http://guba.eastmoney.com/list,000002,f_1.html')
			# print i, 'time:', (time.time() - start), 's  ', response.status_code
		# response = requests.get('http://www.zhihu.com/question/23297146/answer/24202415')

		# pattern = re.compile(ur'共有帖子数 (\d+) 篇')
		# pattern = re.compile(ur'共有')
		# result  = pattern.findall(response.text)
		# print result
		# driver = webdriver.PhantomJS()
		# driver.get('http://guba.eastmoney.com/list,000002,f_1.html')
		# print response.status_code
		# if u'下一页' in response.text:
			# print 'this is here'
		# fp = codecs.open('test.txt', mode='w', encoding='utf-8')
		# fp.write(response.text)
		# fp.write(driver.page_source)
		# fp.close()
		# print i, 'get html'
		# except Exception, e:
			# print str(e)
		# print 'get error'
