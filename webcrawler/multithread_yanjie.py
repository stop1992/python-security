# -*- encoding: utf-8 -*-

import re
import requests
import time
import os
import threading
import Queue
from bs4 import BeautifulSoup
import codecs
from selenium import webdriver
import xlrd

# global variable
MAX_THREADS = 5
OUTPUT_QUEUE = Queue.Queue()  # store gene names
INPUT_QUEUE = Queue.Queue()  # store html data

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
			self.work_queue.put((handle_data, INPUT_QUEUE.get()))

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
		self.driver = webdriver.PhantomJS()
		self.start()

	def run(self):
		while True:
			try:
				func, args = self.work_queue.get(block=False)
				func(args, self.driver)
				# func(args, 'test')
			except Queue.Empty:
				break
			except requests.ConnectionError:
				print 'connection error'
				# while True:
					# try:
						# func(args)
					# except requests.ConnectionError:
						# continue
				continue
	
def get_data():
    data = xlrd.open_workbook('mRNAdata.xls')
    table = data.sheets()[0]
    col_values = table.col_values(7)
    col_len = len(col_values)
    for i in xrange(11, col_len):
		INPUT_QUEUE.put(col_values[i])

def handle_data(gene_name, driver):
	base_url = 'http://www.ncbi.nlm.nih.gov/gene/?term='
	url = base_url + gene_name
	# driver = webdriver.PhantomJS()
	driver.get(url)

	try:
		result_element = driver.find_element_by_xpath('//*[@id="padded_content"]/div[4]/div/h2')
	except:
		print 'no result' 
		return 

	line_numbers = 20
	if len(result_element.text) < 15:
		tmp_text = result_element.text.split()
		line_numbers = int(tmp_text[1])

	for line in xrange(line_numbers):
		line += 1
		xpath = '//*[@id="gene-tabular-docsum"]/div[2]/table/tbody/tr[' + str(line) + ']/td[2]/em'
		exists_homo_sapiens = driver.find_element_by_xpath(xpath)

		if exists_homo_sapiens.text == 'Homo sapiens':
			xpath = '//*[@id="gene-tabular-docsum"]/div[2]/table/tbody/tr[' + str(line) + ']/td[1]/div[2]/a'
			get_gene_href = driver.find_element_by_xpath(xpath)
			url = get_gene_href.get_attribute('href')
			# driver.close()
			# driver.quit()
			# print '\n', url, '\n'
			# driver = webdriver.PhantomJS()
			driver.get(url)
			try:
				gene_type = driver.find_element_by_xpath('//*[@id="summaryDl"]/dd[5]')
				exon_count = driver.find_element_by_xpath('//*[@id="padded_content"]/div[5]/div[2]/div[2]/div[2]/div/dl/dd')
			except:
				print '\n\nerror url:', driver.current_url, '\n\n\n'
				break

			print 'gene_type: ', gene_type.text
			print 'exon_count: ', exon_count.text
			OUTPUT_QUEUE.put(gene_type.text + ' ' + exon_count.text)
			# driver.close()
			# driver.quit()
			break
	# driver.close()
	# driver.quit()

if __name__ == "__main__":
	os.system('printf "\033c"')

	get_data()
	print INPUT_QUEUE.qsize()
	work_manager = WorkManager(INPUT_QUEUE.qsize(), MAX_THREADS)
	work_manager.finish_all_threads()

	print OUTPUT_QUEUE.qsize()

