#-*- coding:utf-8 -*-
#!/usr/bin/env python

import os

def demo(func):
	def _demo():
		print 'before myfunc called'
		func()
		print 'after myfunc called'
	return func

@demo
def myfunc():
	print 'called myfunc func'
	return 'ok'

os.system('printf "\033c"')

print '--------------------------------------------------'
myfunc()
print '---------------------------------------------------'
myfunc()
