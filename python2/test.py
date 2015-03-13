#!/usr/bin/env python

import time
import os
import copy

os.system('printf "\033c"')

class Base:
	def __init__(self, arg1, arg2):
		print 'this is Base __init__ func'

class AddBase(Base):
	def __init__(self, arg1, arg2, arg3):
		Base.__init__(self, arg1, arg2)
		print 'this is AddBase __init__ func'

if __name__ == '__main__':
	addbase = AddBase(1, 2, 3)

#while True:
#	length = raw_input("please enter length: ")
#	try:
#		length = float(length)
#	except:
#		print "input data error, input again"
#		continue
#	else:
#		break
#	
#print length
#def run_time(func):
#	def wrapper(*args, **kwargs):
#		start = time.time()
#		tmp = func()
#		print time.time() - start
#		return tmp
#	return wrapper
#
#@run_time
#def test():
#	print 'just a test   ........'
#
#if __name__ == "__main__":
#	test()
	#print type(test)
	#s = test()
	#print type(s)
	#print s
	#try:
	#	t = float('sldjflk')
	#finally:
	#	print 'arrive here'
	#f = open('test.txt', 'a+')
	#lines = [ line.strip() for line in f.readlines() ]
	#f.close()
	#print lines

	#outFile = open('daitao.txt', 'w')
	#s = 'daitao'
	#outFile.write(s + '\n')
	#outFile.write('\n')
	#outFile.close()
#class Test:
#    ch = 'daitao'
#    def testone(self):
#	    print Test.ch
#
#if __name__ == "__main__":
#		test = Test()
#		test.testone()
#class Test:
#    def daitao(self):
#        pass
#
#    def wangxi(self):
#        print 'this is a test'
#
#if __name__ == "__main__":
#    print 'diatao'
#inputdata = raw_input("please enter:")
#print inputdata
#def add(x, y):
#	return x + y
#def sub(x, y):
#	return x - y
#def mul(x, y):
#	return x * y
#operator = {"+":add, "-":sub, "*":mul}
#print operator.get("*")(2,3)
#indata = raw_input("enter any key to continue\
#		 daitao wang \
#		 xi")
#indataw = raw_input("please enter next key")
#for i in range(0, 10):
#	i += 1
#print i
#for i in range(0, 10):
#	i += 1
#print i
#f = open("file.gb", "r")
#f2 = copy.deepcopy(f)
#alllines = f.readlines()
#print len(alllines)
#alllines2 = f2.readlines()
#print len(alllines2)
#data = [None] * 40000000
#print len(data)
#for i in range(0, 10):
	#print i
#start = time.time()
#s = 0
#i = 0
#fp = open("./file.gb", "r")
#lenth = fp.readlines()
#print len(lenth)
#for eachline in lenth:
#	#print eachline
#	s += i
#	#raw_input()
#end = time.time()
#print end - start
