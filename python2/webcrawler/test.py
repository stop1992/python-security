#!/usr/bin/env python

import os
import Queue
import threading
import Queue

class Base(object):
	tt = 'this is a test'
	rules = ()

	def __init__(self):
		self.data = 'print'
		#print self.tt
	
	def print_rules(self):
		print self.rules

class Derive(Base):
	rules = ['derive set rules','derive']

	def __init__(self):
		super(Derive, self).__init__()
		
if __name__ == '__main__':
	os.system('printf "\033c"')

	#derive = Derive()
	#derive.test()
	base1 = Base()
	base2 = Base()

	derive = Derive()
	base1.print_rules()
