#!/usr/bin/env python

import os
import Queue

class Test:
	def __init__(self, queue):
		self.queue = queue
	def get_element(self):
		try:
			print self.queue.get(block=False)
		except Queue.Empty:
			print 'queue is empty'
if __name__ == '__main__':
	os.system('printf "\033c"')

	q = Queue.Queue()
	q.put('a')
	q.put('b')
	test1 = Test(q)
	test1.get_element()
	test2 = Test(q)
	test2.get_element()

