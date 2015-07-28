#encoding:utf-8

import os
from optparse import OptionParser, OptionGroup

def test1():
	""" this function to test optparse"""
	parser = OptionParser()
	parser.add_option('-u', '--url', dest='url', help='this is webpage you want to go')
	(options, args) = parser.parse_args()
	print options.url, args

if __name__ == '__main__':
	os.system('printf "\033c"')

	test1()
