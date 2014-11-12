#!/usr/bin/env python

import urllib2

def translate(fromLanguage, toLanguagea, language):
	'''you chose a word, then this programs will translate it to
	language you want to translate'''
	userAgent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36"
	url = "http://zhidao.baidu.com/ihome/ask"
	headers = {'User-Agent':userAgent}
	req = urllib2.Request(url, headers=headers)
	try:
		info = urllib2.urlopen(req)
	except urllib2.HTTPError as e:
		# print e.code
		# print e.read()
		print "error"
	print info.read()

fLanguage = "en"
tLanguage = "en"
Language = "en"
translate(fLanguage, tLanguage, Language)

