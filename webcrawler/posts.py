# -*- encoding: utf-8 -*-

import re
import requests
# import time
import os
import threading
import Queue
# from bs4 import BeautifulSoup
import xlrd

# global variable
max_threads = 5
Stock_queue = Queue.Queue()  # store gene names
Html_queue = Queue.Queue()  # store html data

class WorkManager:
    def __init__(self, work_queue_size=1, thread_pool_size=1):
		self.work_queue = Queue.Queue()
		self.thread_pool = [] # initiate, no have a thread
		self.work_queue_size = work_queue_size
		self.thread_pool_size = thread_pool_size
		self.__init_work_queue()
		self.__init_thread_pool()

    def __init_work_queue(self):
		for i in xrange(self.work_queue_size):
			self.work_queue.put((get_html_data, Stock_queue.get()))

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
				print 'connection error:', requests.ConnectionError.message, requests.ConnectionError.errno
				# while True:
					# try:
						# func(args)
					# except requests.ConnectionError:
						# continue
				continue
	
def get_html_data(stock_num):
	url = 'http://guba.eastmoney.com/list,' + stock_num + ',f_1.html'
	response = requests.get(url)
	pattern = re.compile(ur'共有帖子数 (\d+) 篇')
	result = pattern.search(response.text)
	num = 0
	if result:
		num = int(result.group(1))
	print 'stock_num:', stock_num, ' posts_num:', num
	Html_queue.put(num)
		# print i, result.group(1)


def get_stock_num():
	data = xlrd.open_workbook('data.xls')
	table = data.sheets()[0]
	colum_data = table.col_values(1)

	for stock_num in colum_data:
		if stock_num:
			stock_len = len(stock_num)
			for j in xrange(6-stock_len):
				stock_num = '0' + stock_num
			Stock_queue.put(stock_num)

"""
	for i in xrange(1, 7000000):
		stock_num = str(i)
		stock_len = len(stock_num)
		for j in xrange(6-stock_len):
			stock_num = '0' + stock_num
		Stock_queue.put(stock_num)
"""
if __name__ == '__main__':
	os.system('printf "\033c"')
		
	get_stock_num()
	print Stock_queue.qsize()
	# work_manager = WorkManager()
	work_manager = WorkManager(Stock_queue.qsize(), max_threads)
	work_manager.finish_all_threads()

	print Html_queue.qsize()
	stock_nums = Html_queue.qsize()
	total_nums = 0
	for item in xrange(stock_nums):
		total_nums += item
	print 'total posts:', total_nums

