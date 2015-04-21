# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import threading
import Queue
import xlrd
import requests
from bs4 import BeautifulSoup

# global variable
max_threads = 50
Gene_queue = Queue.Queue()  # store gene names
Html_queue = Queue.Queue()  # store html data

class WorkManager:
    def __init__(self, work_queue_size, thread_pool_size):
		self.work_queue = Queue.Queue()
		self.thread_pool = [] # initiate, no have a thread
		self.work_queue_size = work_queue_size
		self.thread_pool_size = thread_pool_size
		self.__init_work_queue()
		self.__init_thread_pool()

    def __init_work_queue(self):
		for i in xrange(self.work_queue_size):
			self.work_queue.put((get_html_data, Gene_queue.get()))

    def __init_thread_pool(self):
		for i in xrange(self.thread_pool_size):
			self.thread_pool.append(WorkThread(self.work_queue))
	
    def finish_all_threads(self):
		for i in xrange(self.thread_pool_size):
			if self.thread_pool[i].is_alive():
				self.thread_pool[i].join()


class WorkThread(threading.Thread):
	def __init__(self, work_queue):
		threading.Thread.__init__(self)
		self.work_queue = work_queue
		self.start()

	def run(self):
		while True:
			try:
				func, args = self.work_queue.get(block=False)
				func(args)
			except Queue.Empty:
				break
			except requests.ConnectionError:
				while True:
					try:
						func(args)
					except requests.ConnectionError:
						continue
				continue
	

def get_html_data(gene_name):
	base_url = 'http://www.ncbi.nlm.nih.gov/gene'
	data = {'term':gene_name}
	html_data = requests.get(base_url, params=data)
	global Html_queue
	Html_queue.put(html_data.text)
	

def get_data_from_excel():
    data = xlrd.open_workbook('mRNAdata.xls')
    table = data.sheets()[0]
    col_values = table.col_values(7)
    global Gene_queue
    for i in xrange(11, table.nrows):
        Gene_queue.put(col_values[i])


class ParseGeneData:
    def __init__(self):
        pass



<<<<<<< HEAD
	get_data_from_excel()
	#print gene_queue.qsize()
	#raw_input('press')
	gene_threads_pool = []
	for i in xrange(max_threads):
		genesearch = GeneSearch(i)
		genesearch.setDaemon(True)
		gene_threads_pool.append(genesearch)
		genesearch.start()

	stop_free_thread_pool()
=======
if __name__ == '__main__':
    os.system('printf "\033c"')
>>>>>>> d9626fb669fc8d43c17223e8e416746ad6122a15

    get_data_from_excel()
    print Gene_queue.qsize()
    work_manager = WorkManager(Gene_queue.qsize(), max_threads)
    work_manager.finish_all_threads()

    print Html_queue.qsize()
