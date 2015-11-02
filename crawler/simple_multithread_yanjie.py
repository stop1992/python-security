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
import httplib

# global variable
MAX_THREADS = 20
OUTPUT_QUEUE = Queue.Queue()  # store gene names
INPUT_QUEUE = Queue.Queue()  # store html data
log_file = open('log.txt', 'w')
lock = threading.Lock()

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
    col_values = table.col_values(2)
    col_len = len(col_values)
    # print col_len
    for i in xrange(1, col_len):
        INPUT_QUEUE.put(col_values[i])
        # if i == col_len - 1:
            # print col_values[i]

def handle_full_report(driver, gene_name, sign, url):
    global lock, log_file
    try:
        driver.get(url)
        # log_file.write('current url: ' +  driver.current_url  + ' ' + gene_name + '\n')
    except httplib.BadStatusLine:
        print 'request full report url error'
        return
    try:
        gene_type = driver.find_element_by_xpath('//*[@id="summaryDl"]/dd[5]')
    except Exception, e:
        # print 'error!! current url: ', driver.current_url  + ' ' + gene_name + ' ' + 'Get gene_type error' +  ' ' + url + '\n'
        # lock.acquire()
        log_file.write('\n---------------------------------------------------\n')
        log_file.write('error!! current url: ' + driver.current_url  + ' ' + gene_name  + ' Get gene_type error ' + url + '\n')
        try:
            driver.get(url)
            gene_type = driver.find_element_by_xpath('//*[@id="summaryDl"]/dd[5]')
        except Exception, e:
            print 'meet a error, in second get url.....'
            print 'erro message:', str(e)
            driver.get_screenshot_as_file('./' + gene_name + '.png')
            return
            # log_file.write('changed current url: ' + driver.current_url  + ' ' + gene_name  + ' Get gene_type error ' + url + '\n')
            # print traceback.print_exc()
        # lock.release()
    # lock.release()

    try:
        print 'gene_name:', gene_name, 'gene_type:', gene_type.text
        OUTPUT_QUEUE.put(gene_name + ' ' + gene_type.text)
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

    line_numbers = 20
    for line in xrange(line_numbers):
        line += 1
        xpath = '//*[@id="gene-tabular-docsum"]/div[2]/table/tbody/tr[' + str(line) + ']/td[2]/em'
        try:
            exists_homo_sapiens = driver.find_element_by_xpath(xpath)
        except Exception, e:
            continue

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

def main():

    start = time.time()
    get_data()
    print INPUT_QUEUE.qsize()
    work_manager = WorkManager(INPUT_QUEUE.qsize(), MAX_THREADS)
    work_manager.finish_all_threads()

    print OUTPUT_QUEUE.qsize()

    fp = codecs.open('result.txt', mode='w', encoding='utf-8')
    while OUTPUT_QUEUE.qsize() > 0:
        element = OUTPUT_QUEUE.get()
        fp.write(element+'\n')
    fp.close()
    print 'use time:', time.time() - start

def test():
    get_data()

if __name__ == "__main__":
    os.system('printf "\033c"')
    os.system('rm -rf *.png')

    # test()
    main()
