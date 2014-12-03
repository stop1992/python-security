#!/usr/bin/env python

import urllib2
import urllib
import cookielib
import re
from bs4 import BeautifulSoup

class Email163:
	header = None
	opener=None
	data=None
	
	# some function
	def __init__(self, agent):
		my_agent = agent
		self.header = {'User-Agent':my_agent}
		self.cookie = cookielib.CookieJar()
		cookiehandler = urllib2.HTTPCookieProcessor(self.cookie)
		urllib2.install_opener(urllib2.build_opener(cookiehandler))

	def login(self, username, passwd):
		'''
			login
		'''
		postdata = urllib.urlencode({
				'savelogin':0,
				'url2':"http//mail.163.com/errorpage/error163.htm",
				'username':username,
				'password':passwd
				})
		req = urllib2.Request(
					url = "https://mail.163.com/entry/cgi/ntesdoor?df=mail163_letter&from=web&funcid=loginone&iframe=1&language=-1&passtype=1&product=mail163&net=c&style=-1&race=58_72_223_gz&uid="+username,#pdmtestmail@163.com"
					data=postdata,
					headers=self.header)
		#cookielib.CookieJar.add_cookie_header(req)
		self.beforedata = urllib2.urlopen(req, timeout=20)
		self.data = self.beforedata.read()

	def relogin(self, url):
		req = urllib2.Request(url = url, headers = self.header)
		self.data = urllib2.urlopen(req, timeout=20).read()


if __name__ == "__main__":
	agent="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36"
	mail163=Email163(agent)
	mail163.login('pdmtestmail@163.com', 'testtest')
	#htmlfile = open("mail.html", "w")
	#htmlfile.write(mail163.data)
	
	#htmlfile.close()
	#print mail163.beforedata.geturl()
	#print mail163.beforedata.info()
	#print mail163.data
	soup = BeautifulSoup(mail163.data)
	script = soup.find("script")
	content = re.split('"', repr(script.contents))
	mail163.relogin(content[1])
	print mail163.data
	#print mail163.data.geturl()
	#print mail163.data.info()
