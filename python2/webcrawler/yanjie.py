#-*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import xlrd
import requests
from bs4 import BeautifulSoup
import threading
from Queue import Queue
#import codecs

class GeneSearch(threading.Thread):
	def __init__(self, gene_name, num):
		threading.Thread.__init__(self)
		self.base_url = 'http://www.ncbi.nlm.nih.gov/gene'
		self.gene_name = gene_name
		self.num = num

	#def get_data(self):
	def run(self):
		data = {'term':self.gene_name}
		response = requests.get(self.base_url, params=data)
		global queue
		queue.put(response.text)
		print 'thread', self.num, 'over'
		#fp = codecs.open('html.txt', 'w', 'utf-8')
		#fp.write(response.text)
		#fp.close()
		#print response.text
		#raw_input('press any key to continue')
		#print response.encoding
		


def get_data_from_excel():
	data = xlrd.open_workbook('mRNAdata.xls')
	table = data.sheets()[0]
	col_values = table.col_values(7)
	gene_names = []
	for i in xrange(11, table.nrows):
		gene_names.append(col_values[i])
		#tmp_set.add(col_values[i])
	return gene_names

class ParseGeneData:
	def __init__(self):
		pass

queue = Queue()
if __name__ == '__main__':
	os.system('printf "\033c"')

	gene_names = get_data_from_excel()
	gene_len = len(gene_names)
	#print gene_len
	#for i in xrange(gene_len):
	for i in xrange(60):
		genesearch = GeneSearch(gene_names[i], i)
		genesearch.start()
		#genesearch.get_data()
	#for i in xrange(gene_name):
	for i in xrange(60):
		genesearch.join()

	print queue.qsize()
