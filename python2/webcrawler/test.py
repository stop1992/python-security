#!/usr/bin/env python

import os
import Queue
import threading
import Queue

thread_queue = Queue.Queue()


class ThreadTest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        thread_queue.put(self)


if __name__ == '__main__':
	#os.system('printf "\033c"')
	tmp_list = []
	for i in xrange(10000000):
		tmp_list.append(i)

	tmp_len = len(tmp_list)
	#for i in xrange(tmp_len):
	for i in xrange(len(tmp_list)):
		tmp_list[i] = 'test'
		pass
	
	print len(tmp_list)
