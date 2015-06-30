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

if __name__ == '__main__':
	os.system('printf "\033c"')

	test3()
	
	# client = MongoClient('192.168.1.108', 27018)
	# db = client['web']
	# teacher = db['teacher']
	# teacher = db['student']
	# tmp = teacher.find()
	# print tmp
	# result = teacher.find_one_and_update({'name':'daitao'}, {'$set':{'age':66}})
	# result = teacher.find_one({'name':'daitao'})
	# print result
	# print result['age']
	# a = {'test':3, 'daitao':5, 'wangxi':9}
	# b = {'test':5, 'daitao':9, 'wangxi':2, 'bruce':8}
	# c = dict_plus(a, b)
	# print c
