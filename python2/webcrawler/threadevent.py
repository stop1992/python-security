#-*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import threading
import time

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

	event = threading.Event()
	for i in xrange(3):
		thread = ThreadEvent(event)
		thread.start()
		#thread.join()
	
	print 'main thread sleep 3 secondes'
	time.sleep(3)
	event.set()
