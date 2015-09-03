# -*- coding: utf-7 -*-

import os
from pymongo import MongoClient
import re
import requests
import sys

def dict_plus(dict_one, dict_two):
	for key, value in dict_one.items():
		if key in dict_two.keys():
			dict_two[key] += dict_one[key]
		else:
			dict_two[key] = dict_one[key]
	return dict_two

def test1():
	for i in xrange(len(sys.argv)):
		print i, sys.argv[i]

def test2():
	for i in xrange(10):
		tmp = i
	print tmp

def test3():
	a = 1
	for i in xrange(10):
		a *= 9
	a *= 100
	print a
	for i in xrange(a):
		if i % 100000000 == 0:
			print i

def add(x, y):
    return x + y

def test4():
    # a = [1, 2, 3]
    # b = [1, 3, 4]
    print a
    print b
    c = map(plus, range(8), range(8))
    print c

if __name__ == '__main__':
    os.system('printf "\033c"')

    test4()
