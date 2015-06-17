# -*- encoding: utf-8 -*-

import re
import requests
import time
import os
import threading
import Queue
import codecs
from selenium import webdriver
import xlrd
import types
import traceback

# global variable
MAX_THREADS = 10
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
				if type(args) == types.FloatType:
					continue
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

def handle_full_report(driver, gene_name, sign, url):
	try:
		driver.get(url)
	except httplib.BadStatusLine:
		print 'request full report url error'
		return
	try:
		gene_type = driver.find_element_by_xpath('//*[@id="summaryDl"]/dd[5]')
	except:
		print '\n' + sign + ' error url:', driver.current_url  + ' ' + gene_name + ' ' + 'Get gene_type error' +  ' ' + url + '\n'
		return 
	try:
		exon_count = driver.find_element_by_xpath('//*[@id="padded_content"]/div[5]/div[2]/div[2]/div[2]/div/dl/dd')
	except:
		print '\nerror url:', driver.current_url  + '\t' + gene_name + 'get exon_count erro' + '\n'
		return 

	try:
 		relate_articles = driver.find_elements_by_class_name('generef-link')
		# relate_articles = driver.find_element_by_xpath('//*[@id="padded_content"]/div[5]/div[2]/div[4]/div[2]/div[1]/div/ol')
	except Exception, e:
		print 'get relate_articles error'
		print str(e)

	relate_articles_nums = 0
	try:
		if relate_articles[0]:
			relate_articles_nums = unicode(len(relate_articles[0].find_elements_by_tag_name('li')))
	except Exception, e:
		print 'get relate_article_len error'
		print str(e)

	pattern = re.compile(ur'See all (\d+) citations in')
	result = pattern.search(driver.page_source)
	if result:
		relate_articles_nums = result.group(1)

	try:
		print 'gene_type:', gene_type.text + '\t' +  'exon_count:' + exon_count.text + '\t' + 'article_nums:', relate_articles_nums
		OUTPUT_QUEUE.put(gene_name + ' ' + gene_type.text + ' ' + exon_count.text + ' ' + relate_articles_nums)
	except Exception, e:
		print str(e)
		print driver.current_url
	return 

def handle_data(gene_name, driver):
	base_url = 'http://www.ncbi.nlm.nih.gov/gene/?term='
	first_url = base_url + gene_name

	response = requests.get(first_url)
	if len(re.findall(ur'Full Report', response.text)) > 0:
		handle_full_report(driver, gene_name, 'first', first_url)
		print 'excute handle_full_report'
		return
		
	driver.get(first_url)
	try:
		result_element = driver.find_element_by_xpath('//*[@id="padded_content"]/div[4]/div/h2')
	except Exception, e:
		print str(e)
		print 'get result_element error, gene_name:', gene_name ,  ' error url:', driver.current_url
		# print traceback.print_exc()

	line_numbers = 20
	try:
		if len(result_element.text) < 15:
			tmp_text = result_element.text.split()
			line_numbers = int(tmp_text[1])
	except Exception, e:
		print str(e)
		print driver.current_url

	for line in xrange(line_numbers):
		line += 1
		xpath = '//*[@id="gene-tabular-docsum"]/div[2]/table/tbody/tr[' + str(line) + ']/td[2]/em'
		try:
			exists_homo_sapiens = driver.find_element_by_xpath(xpath)
		except Exception, e:
			continue
			# print

		if exists_homo_sapiens.text == 'Homo sapiens':
			xpath = '//*[@id="gene-tabular-docsum"]/div[2]/table/tbody/tr[' + str(line) + ']/td[1]/div[2]/a'
			get_gene_href = driver.find_element_by_xpath(xpath)
			second_url = get_gene_href.get_attribute('href')
			if second_url:
				# driver.get(second_url)
				handle_full_report(driver, gene_name, 'second', second_url)
			else:
				print 'second url none'
			break

if __name__ == "__main__":
	os.system('printf "\033c"')

	start = time.time()
	get_data()
	print INPUT_QUEUE.qsize()
	work_manager = WorkManager(INPUT_QUEUE.qsize(), MAX_THREADS)
	work_manager.finish_all_threads()

	print OUTPUT_QUEUE.qsize()

	fp = codecs.open('result.txt', mode='w', encoding='utf-8')
	# fp.write('gene_name'
	while OUTPUT_QUEUE.qsize() > 0:
		element = OUTPUT_QUEUE.get()
		fp.write(element+'\n')
	fp.close()
	print 'use time:', time.time() - start
