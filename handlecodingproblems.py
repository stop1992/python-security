#!/usr/bin/env python
#coding:utf-8

import urllib2
import chardet
import sys
import codecs

''' this is for test
	utf-8 code
'''
sysencoding = sys.getfilesystemencoding()
print 'sysencoding: %s ' % sysencoding 


reponse = urllib2.urlopen("http://www.baidu.com").read();

#delete BOM
#if reponse[:3] == codecs.BOM_UTF8:
#	reponse = reponse[3:]

mychar=chardet.detect(reponse)
infocoding=mychar['encoding']
print "infocoding sytle: %s" % infocoding

# decode to utf-8 then encode to gbk
print reponse.decode(infocoding, 'ignore').encode('gbk', 'ignore')
