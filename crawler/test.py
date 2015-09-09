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
import threading
from Queue import Queue

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
            print i, 'is float'
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
            # OUTPUT_QUEUE.put(gene_name + ' ' + gene_type.text + ' ' + exon_count.text + ' ' + relate_articles_nums)
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
    """
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

    """
    line_numbers = 20
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

def test5():
    stock_num = '000001'
    url = 'http://guba.eastmoney.com/list,' + stock_num + ',f_1.html'
    print url
    print 'start request....'
    response = requests.get(url)
    print 'end request....'
    pattern = re.compile(ur'共有帖子数 (\d+) 篇')
    result = pattern.search(response.text)
    num = 0
    if result:
        num = int(result.group(1))
    print 'stock_num:', stock_num, ' posts_num:', num
    # print i, result.group(1)


def test7():
    queue = Queue.Queue()
    queue.put('test')
    print queue.qsize()
    print queue.get()
    print queue.qsize()

def test8():
    a = [u'代涛', u'王喜', u'daitao', u'wangxi']
    b = u'代涛 王喜 wangxi daitao'
    for item in a:
        print item
        pattern = re.compile(item)
        result = pattern.findall(b)
        if result:
            for i in result:
                print i, 'in b'

def test9():
    response = requests.get('http://guba.eastmoney.com/news,000002,198611273.html')
    # key_words to store key words, last element to count post amounts
    # key_words = [, 'post_amounts']
    # key words occur times amounts
    # key_words_times = dict.fromkeys(key_words, 0)
    asktime = response.xpath(u'//*[@id="zwconttb"]/div[2]/text()').extract()
    if asktime:
        # from asktime get ask_time
        ask_time = asktime[0].split()[1]
        # from url get stock_num
        stock_num = response.url.split(',')[1]
        print ask_time
        print stock_num
        # compute key_words occur times in response.body
        # for item in key_words:
            # print item
            # pattern = re.compile(item)
            # result = pattern.findall(response.body_as_unicode())
            # if result:
                # every item occur times in response.body
                # key_word_times = len(result)
                # sum up every key word
                # key_words_times[item] += key_word_times
        # key_words_times['key_word_times'] = 1 # represent post one time
        # item['key_words'] = key_words_times
    # else:
            # item['asktime'] =  'null'
            # item['stock_num'] = 'null'

# yield item

def test10(tmp):

    print type(tmp)

def test11(power, *args):
    total = 0
    for i in args:
        total += pow(i, power)
    return total

def test12(**power):
    print type(power)
    print power
    # for i in power.items:
        # print i


def test14():
    queue = Queue()
    for i in xrange(5):
        queue.put('this is a test' + '\n')

    while queue.qsize() > 0:
        print queue.get()
    print 'all done....'

def test15():
    total = 0
    for stock_num in open('num.txt'):
        # print stock_num
        # raw_input('please')
        url = 'http://guba.eastmoney.com/list,' + stock_num.strip() + ',f_1.html'
        response = requests.get(url)
        pattern = re.compile(ur'共有帖子数 (\d+) 篇')
        result = pattern.search(response.text)
        num = 0
        if result:
            num = int(result.group(1))
            total += num
        # print num
    print 'total: ', total


if __name__ == '__main__':
    os.system('printf "\033c"')

    test15()
