#-*-coding:utf-8-*-
#!/usr/bin/env python

import urllib2
import os
import cookielib
import urllib
import re
import types
import time
import requests

import mythread


if __name__ == '__main__':
	os.system('printf "\033c"')

	data = {'username':'2014544007', 'password':'709860'}
	session = requests.Session()
	response = session.post('http://gim.jlu.edu.cn/check.jsp', data=data)
	score = session.get('http://gim.jlu.edu.cn/pyc/menu_stu.jsp?menu=xuanke_check')
	print res.text
