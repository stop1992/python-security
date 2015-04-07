#-*- utf-8 -*-
#!/usr/bin/env python

import re
import os
import urllib
import urllib2
import cookielib
import chardet

class JiLinU:
	def __init__(self, url):
		self.url = url
	
	def get_data(self):
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		urllib2.install_opener(opener)
		data = {
			'usrname':'2014544007',
			'password':'709860'
		};
		postdata = urllib.urlencode(data)
		header = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36' }
		req = urllib2.Request(
				url = self.url,
				data = postdata,
				headers = header)
		result = opener.open(req)
		result_student = opener.open('http://gim.jlu.edu.cn/student.jsp')
		content_student = result_student.read()
		content_student = unicode(content_student, 'GB2312')
		content_student.encode('utf-8')

		print content_student
		#coding = chardet.detect(content)['encoding']
		#print type(content)
		#content.decode(coding, 'ignore').encode('utf-8', 'ignore')
		#content.decode('utf-8', 'ignore')
		#print type(content)
		#print content

	def extract_data(self):
		pass

if __name__ == '__main__':
	os.system('printf "\033c"')

	url = 'http://gim.jlu.edu.cn/check.jsp'
	jilinu = JiLinU(url)
	jilinu.get_data()

