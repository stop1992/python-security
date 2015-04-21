# -*- encoding:utf-8 -*-

import os

def test1():
	for i in xrange(10):
		#print i
		yield test2(i)

	for i in xrange(10, 20):
		yield test2(i)


def test2(arg):
	return arg


if __name__ == '__main__':
	os.system('printf "\033c"')

	test1()
	gen = test1()
	print type(gen)
	for i in gen:
		print i
