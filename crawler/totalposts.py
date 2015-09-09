#!/usr/bin/env python
# encoding: utf-8

import re
import requests
import time
import os
import threading
import multiprocessing
import Queue as Queue_Queue
from multiprocessing import Queue, Pool
from bs4 import BeautifulSoup
import xlrd
import traceback

# global variable
max_threads = 5
Stock_queue = Queue()  # store gene names
stock_post_num = multiprocessing.Queue()

class WorkManager:
    def __init__(self, work_queue_size=1, thread_pool_size=1):
        self.work_queue = Queue()
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
        while self.work_queue.qsize() > 0:
            try:
                func, args = self.work_queue.get(block=False)
                func(args)
            except Queue_Queue.Empty:
                print 'work_queue is empty...'

def get_html_data(stock_num):
        url = 'http://guba.eastmoney.com/list,' + stock_num + ',f_1.html'
        response = requests.get(url)
        pattern = re.compile(ur'共有帖子数 (\d+) 篇')
        result = pattern.search(response.text)
        num = 0
        if result:
            num = int(result.group(1))
        print 'stock_num:', stock_num, ' posts_num:', num
        stock_post_num.put(num)
        # stock_post_num.put('stock_num: ' + str(stock_num) + ' posts_num: ' + str(num))


def get_stock_num():

    for i in xrange(1, 100000):
        i_len = len(str(i))
        stock_num = ''
        for j in xrange(1, 6 - i_len + 1):
            stock_num += '0'
        stock_num += str(i)
        Stock_queue.put(stock_num)

def get_stock_num_from_file():

    data = xlrd.open_workbook('stocknum.xlsx')
    sheet = data.sheets()[3]
    nrows =  sheet.nrows
    for i in xrange(nrows):
         stock = sheet.cell(i, 0).value
         tmp_split = stock.split('.')
         if tmp_split:
             stock_num = tmp_split[0]
             Stock_queue.put(stock_num)
    # fp = open('stocknum.txt', 'w')
    # while Stock_queue.qsize() > 0:
        # fp.write(Stock_queue.get() + '\n')
    # fp.close()
    # for i in xrange(2450):
        # Stock_queue.get()

def get_stock_num_from_txt():
    for stock_num in open('num.txt'):
        Stock_queue.put(stock_num.strip())

def handle(process_name):
    print process_name, 'is running...'
    work_manager = WorkManager(Stock_queue.qsize()/3, max_threads)
    work_manager.finish_all_threads()


def main():

    get_stock_num_from_txt()
    pools = multiprocessing.Pool()
    for i in xrange(3):
        # pools.apply_async(get_html_data, args=('process_'+str(i),))
        pools.apply_async(handle, args=('process_'+str(i),))
    pools.close()
    pools.join()
    print '----------------------------------------'
    total = 0
    while stock_post_num.qsize() > 0:
        total += stock_post_num.get()
    print 'total:', total


def write2txt():

    fp = open('stocknum.txt', 'w')
    global stock_post_num
    print 'stock_post_num: ', stock_post_num.qsize()
    while stock_post_num.qsize() > 0:
        data = stock_post_num.get()
        fp.write(data+'\n')
    fp.close()


if __name__ == '__main__':
    os.system('printf "\033c"')

    main()
