import os
import requests
from collections import defaultdict
from selenium import webdriver

if __name__ == '__main__':
	os.system('printf "\033c"')

	# result = defaultdict(list)

	# a = ['test', 'daitao', 'wangxi', 'test', 'test', 'wangxi', 'bruce', 'lee', 'daitao']
	# b = ['test', 'daitao', 'wangxi', 'bruce', 'lee']
	# result = dict.fromkeys(a, 0)

	# for item in a:
		# result[item] += 1
	# url = 'http://www.ncbi.nlm.nih.gov/gene'
	url = 'http://www.ncbi.nlm.nih.gov/gene/335'
	for i in xrange(6000):
		# requests.get('http://www.ncbi.nlm.nih.gov/gene')
		driver = webdriver.PhantomJS()
		driver.get(url)
		print 'open success'
		driver.close()
		driver.quit()

	print result
