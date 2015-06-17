# encoding:utf-8

import re
import requests
import os
import sys
import xlrd
import xlwt


def test1():
	fp = open('data.txt', 'r')
	data = fp.readlines()
	pattern = re.compile(r'mRNA: NM_000927:  (\d+)~(\d+)')
	result = pattern.findall(str(data))
	print len(data)
	for item in result:
		print type(item)
		print item[0], item[1]
		raw_input('press any key')
	print len(result)

def test2():
	fp = open('mRNA.txt', 'r')
	line = fp.readline()
	print len(line)
	print line
	for i in xrange(len(line) - 1):
		if line[i]:
			print '\n---------'
			print i, line[i]
			print '---------'
		else:
			print 'this is null'
			raw_input('press any key')

if __name__ == '__main__':
	os.system('printf "\033c"')

	test2()


