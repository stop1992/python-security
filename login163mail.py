#!/usr/bin/env python

import urllib2
import urllib

postdata=urllib.urlencode({
	'username':"pdmtestmail@163.com",
	'password':"testtest"
	})
req = urllib2.Request(
		url = "http://mail.163.com/",
		data = postdata
		)
files = open("/cygdrive/d/test/test.txt", "w")
result = urllib2.urlopen(req).read()
files.write(result)
files.close()
