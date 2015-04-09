#-*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import xlrd
import requests
from bs4 import BeautifulSoup
import threading
from Queue import Queue
#import codecs

max_threads = 10

class GeneSearch(threading.Thread):
	def __init__(self, num):
		threading.Thread.__init__(self)
		self.base_url = 'http://www.ncbi.nlm.nih.gov/gene'
		self.num = num

	#def get_data(self):
	def run(self):
		global gene_queue
		while True:
			gene_name = gene_queue.get()
			print gene_name
			if gene_name == 'stop':
				print 'thread', self.num, 'over'
				break
			else:
				data = {'term': gene_name}
				response = requests.get(self.base_url, params=data)
				global html_queue
				html_queue.put(response.text)

def get_data_from_excel():
	data = xlrd.open_workbook('mRNAdata.xls')
	table = data.sheets()[0]
	col_values = table.col_values(7)
	global gene_queue
	for i in xrange(11, table.nrows):
		gene_queue.put(col_values[i])

def stop_free_thread_pool():
	global gene_queue
	for i in xrange(max_threads):
		gene_queue.put('stop')

class ParseGeneData:
	def __init__(self):
		pass

gene_queue = Queue() # store gene names 
html_queue = Queue() # store html data 

if __name__ == '__main__':
	os.system('printf "\033c"')

	get_data_from_excel()
	print gene_queue.qsize()
	#raw_input('press')
	gene_threads_pool = []
	for i in xrange(max_threads):
		genesearch = GeneSearch(i)
		genesearch.setDaemon(True)
		gene_threads_pool.append(genesearch)
		genesearch.start()

	stop_free_thread_pool()

	for i in xrange(max_threads):
		gene_threads_pool[i].join()

	print html_queue.qsize()
