#-*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import threading
import time
import Queue

class ThreadEvent(threading.Thread):
	def __init__(self, event):
		threading.Thread.__init__(self)
		self.event = event
	
	def run(self):
		print 'this is ', self.name, ', will waiting'
		self.event.wait()
		print self.name, 'wait finished'
	
if __name__ == '__main__':
	os.system('printf "\033c"')

	#event = threading.Event()
	#event_queue = Queue.Queue()
	event_list = []
	for i in xrange(30):
		event = threading.Event()
		event_list.append(event)

	for i in xrange(30):
		thread = ThreadEvent(event_list[i])
		thread.start()
	
	print 'main thread sleep 3 secondes'
	time.sleep(3)
	for i in xrange(20):
		event_list[i].set()
