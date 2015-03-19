#!/usr/bin/env python

import os
import threading
from time import sleep, time

loops = [4,2]

class ThreadFunc(object):

	def __init__(self, func, args, name=''):
		self.name = name
		self.func = func
		self.args = args
	
	def __call__(self):
		apply(self.func, self, args)
	
def loop(nloop, sec):
	print 'start loop', nloop, 'at:', ctime()
	sleep(sec)
	print 'end loop', nloop, 'at:', ctime()

def main():
	print 'startring at:', ctime()
	threads = []
	nloops = range(len(loops))

	for i in nloops:
		t = threading.Thread(
				target=ThreadFunc(loop, (i, loops[i]),loop.__name__))
		threads.append(t)
	
	for i in nloop:
		threads[i].start()

	for i in nloop:
		threads[i].join()

	print 'all DONE at:', ctime()

if __name__ == '__main__':
	os.system('printf "\033c"')
	main()
