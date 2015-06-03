# -*- coding: utf-8 -*-  

import os

class Test(object):
	def __init__(self, data):
		self.server = data

	def __len__(self):
		return 3

class Tt(Test):
	def pp(self):
		print self.server

if __name__ == '__main__':
	os.system('printf "\033c"')

	# print 'test'
	cmd = 'ls --color'
	os.system(cmd)

	# test = Inherit()
	# test.one()
	# test = Test('test is test')
	# t = Tt()
	# t.pp()
	# print len(test)
