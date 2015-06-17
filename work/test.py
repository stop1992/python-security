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


if __name__ == '__main__':
	os.system('printf "\033c"')

	test1()


