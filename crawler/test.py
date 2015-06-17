#-*- encoding:utf-8 -*-

import xlrd
import os
import requests
from collections import defaultdict
import xlrd
from selenium import webdriver
import types
import re
from redis import Redis
from pymongo import MongoClient
import time

def get_data():
    data = xlrd.open_workbook('mRNAdata.xls')
    table = data.sheets()[0]
    col_values = table.col_values(7)
    col_len = len(col_values)
    print col_len - 11
    sum_float = 0
    for i in xrange(11, col_len):
		# print type(col_values[i])
		if type(col_values[i]) == types.FloatType:
			sum_float += 1
    print sum_float
    print col_len - 17

def test():
	url = 'http://www.ncbi.nlm.nih.gov/gene/34'
	# url = 'http://www.ncbi.nlm.nih.gov/gene/?term=ACADM'
	driver = webdriver.PhantomJS()
	driver.get(url)
	try:
		# relate_articles = driver.find_element_by_xpath('//*[@id="padded_content"]/div[5]/div[2]/div[4]/div[2]/div[1]/div/ol')
		# relate_articles = driver.find_element_by_css_selector('#padded_content > div.rprt.full-rprt > div.rprt-body > div.rprt-section.gene-bibliography > div.rprt-section-body > div:nth-child(1) > div > ol')
		# a = driver.find_element_by_css_selector('#padded_content > div.rprt.full-rprt > div.rprt-body > div.rprt-section.gene-bibliography > div.rprt-section-body > div:nth-child(1) > div > ol')
		relate_articles = driver.find_elements_by_class_name('generef-link')
	except Exception, e:
		print 'get relate_articles error'
		print str(e)
	
	# print type(a)
	try:
		if relate_articles[0]:
			relate_articles_nums = len(relate_articles[0].find_elements_by_tag_name('li'))
			print 'relate_articles_li:', relate_articles_nums
			print type(relate_articles_nums)
	except Exception, e:
		print 'len error'
		print str(e)

	pattern = re.compile(ur'See all (\d+) citations in')
	result = pattern.search(driver.page_source)
	if result:
		relate_articles_nums = result.group(1)
	print result.group(1)
	print type(relate_articles_nums)

def test_gene_type():
	url = 'http://www.ncbi.nlm.nih.gov/gene/?term=RPL38'
	driver = webdriver.PhantomJS()
	driver.get(url)

	try:
		result_element = driver.find_element_by_xpath('//*[@id="padded_content"]/div[4]/div/h2')
	except Exception, e:
		print str(e)
		print traceback.print_exc()

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
			second_url = get_gene_href.get_attribute('href')
			print second_url
			if second_url:
				driver.get(second_url)
				print driver.current_url
				# handle_full_report(driver, gene_name, 'second')
			else:
				print 'second url none'
			break


def test2():
	url = 'http://www.ncbi.nlm.nih.gov/gene/2811'
	response = requests.get(url)
	result = re.findall(ur'Full Report', response.text)
	if result:
		print result

def test3():
	url = 'http://www.ncbi.nlm.nih.gov/pubmed/?term=FXN'
	# response = requests.get(url)
	driver = webdriver.PhantomJS()
	driver.get(url)
	# print response.text
	result = re.findall(ur'articles about FXN gene function', driver.page_source)
	if result:
		print result

def test4():
	driver = webdriver.PhantomJS()
	driver.get('http://www.baidu.com')
	driver.close()
	driver.get('http://www.taobao.com')
	
if __name__ == '__main__':
	os.system('printf "\033c"')

	test4()
