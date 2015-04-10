#-*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import threading
import Queue
import xlrd
import requests
import urllib2

class ThreadManager:
	def __init__(self, work_queue_size, thread_pool_size):
		self.work_queue = Queue.Queue()
		self.thread_pool = []
		self.__init_work_queue(work_queue_size)
		self.__init_thread_pool(thread_pool_size)

	def __init_work_queue(self, work_queue_size):
		for i in xrange(work_queue_size):
			self.work_queue.put((get_html_data, Gene_queue.get()))

	def __init_thread_pool(self, thread_pool_size):
		for i in xrange(thread_pool_size):
			self.thread_pool.append(Thread(self.work_queue))

	def wait_all_threads_done(self):
		for i in xrange(len(self.thread_pool)):
			if self.thread_pool[i].isAlive():
				self.thread_pool[i].join()

class Thread(threading.Thread):
	def __init__(self, work_queue):
		#super(Thread, self).__init__(self)
		threading.Thread.__init__(self)
		self.work_queue = work_queue
		self.start()
	
	def run(self):
		while True:
			try:
				func, args = self.work_queue.get(block=False)
				func(args)
				print 'thread over'
				#self.work_queue.task_done()
			except Queue.Empty:
				print 'queue is empty'
				break
			except Exception, e:
				print 'thread start error'
				print e.message
				print e
				break


def get_data_from_excel():
	#data = xlrd.open_workbook('mRNAdata.xls')
	#table = data.sheets()[0]
	#col_values = table.col_values(7)
	url = 'http://www.baidu.com'
	global Gene_queue
	#for i in xrange(11, table.nrows):
	for i in xrange(11, 300):
		Gene_queue.put(url)

def get_html_data(gene_name):
	#base_url = 'http://www.ncbi.nlm.nih.gov/gene'
	#data = {'term': gene_name}
	#response = requests.get(base_url, params=data)
	#response = requests.get(gene_name)
	res = urllib2.urlopen(gene_name)
	text = res.read()
	global Html_queue
	#Html_queue.put(response.text)
	Html_queue.put(text)

# global variable
Gene_queue = Queue.Queue()
Html_queue = Queue.Queue()

if __name__ == '__main__':
	os.system('printf "\033c"')

	get_data_from_excel()
	print Gene_queue.qsize()
	thread_manager = ThreadManager(Gene_queue.qsize(), 50)
	thread_manager.wait_all_threads_done()
	print Html_queue.qsize()
