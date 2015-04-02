#!/usr/bin/env python

import os

def func_one():
	count = 2
	def func_three():
		nonlocal count 
		count += 1
		print count

def func_two():
	count = 1
	print count

if __name__ == '__main__':
	os.system('printf "\033c"')

	func_one()
	func_two


