#!/usr/bin/env python

import time
import os
import copy
from random import choice

os.system('printf "\033c"')

class Base:
	def __init__(self, arg1, arg2):
		print 'this is Base __init__ func'

class AddBase(Base):
	def __init__(self, arg1, arg2, arg3):
		Base.__init__(self, arg1, arg2)
		print 'this is AddBase __init__ func'

class TestStaticMethod:
	def foo():
		print 'calling static method foo()'

		foo = staticmethod(foo)

class TestClassMethod:
	def foo(cls):
		print 'calling class method foo()'
		print 'foo() is part of class:', cls.__name__

class RoundFloatManual(object):
	def __init__(self, val):
		assert isinstance(val, float), \
			"value must be float!"
		self.value = round(val, 2)
	def __str__(self):
		return str(self.value)

class Time60(object):
	def __init__(self, hr, mini):
		self.mini = mini
		self.hr = hr
		#print 'enter Time60 function'

	def __str__(self):
		return '%d:%d' % (self.hr, self.mini)

	__repr__ = __str__

	def __add__(self, other):
		return self.__class__(self.hr + other.hr, self.mini +other.mini)
	
	def __iadd__(self, other):
		self.hr += other.hr
		self.mini += other.mini
		return self

class RandSeq(object):
	def __init__ (self, seq):
		self.data = seq
	
	def __iter__ (self):
		return self
	
	def next(self):
		return choice(self.data)

class AnyIter(object):
	def __init__ (self, data, safe=False):
		self.safe = safe 
		self.iter = iter(data)
	
	def __iter__ (self):
		return self
	
	def next(self, howmany=1):
		retval = []
		for eachItem in range(howmany):
			try:
				retval.append(self.iter.next())
			except StopIteration:
				if self.safe:
					break
				else:
					raise
		return retval

class WrapMe(object):
	def __init__ (self, obj):
		self.__data = obj
	def get(self):
		return self.__data
	def __repr__ (self):
		return self.__data
	def __str__ (self):
		return str(self.__data)
	def __getattr__ (self, attr):
		return getattr(self.__data, attr)

class Descriptor(object):
	def __get__(self, object, type):
		print 'get', self, object, type
	
	def __set__(self, object, value):
		print 'set', self, object, value

class Demo(object):
	desc = Descriptor()

class Test:

	@classmethod
	def test(cls):
		print 'this is class method'

	@staticmethod
	def static_method():
		print 'this is a static method'

	def instance_method(self):
		print 'this is a instance method'

if __name__ == '__main__':
	os.system('printf "\033c"')

	t = Test()
	t.test()
	t.static_method()
	t.instance_method()
