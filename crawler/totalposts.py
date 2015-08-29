# -*- encoding: utf-8 -*-

import re
import requests
import time
import os
import threading
import Queue
from bs4 import BeautifulSoup
import xlrd

# global variable
max_threads = 15
Stock_queue = Queue.Queue()  # store gene names
Html_queue = Queue.Queue()  # store html data

class WorkManager:
    def __init__(self, work_queue_size=1, thread_pool_size=1):
        # print work_queue_size, thread_pool_size
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
        # print self.work_queue.qsize()
        self.start()
        # print 'after starting'

    def run(self):
        # print 'test'
        while True:
            try:
                func, args = self.work_queue.get(block=False)
                print args
                func(args)
            except Queue.Empty:
                # print 'work queue is empty'
                break
            except requests.ConnectionError:
                print 'connection error'
                # while True:
                        # try:
                                # func(args)
                        # except requests.ConnectionError:
                                # continue
                continue

def get_html_data(stock_num):
    url = 'http://guba.eastmoney.com/list,' + stock_num + ',f_1.html'
    response = requests.get(url)
    # print response
    pattern = re.compile(ur'共有帖子数 (\d+) 篇')
    result = pattern.search(response.text)
    num = 0
    if result:
        num = int(result.group(1))
    print 'stock_num:', stock_num, ' posts_num:', num
    if num < 2000:
        raw_input('please enter')
    Html_queue.put(num)
    # print i, result.group(1)


def get_stock_num():

    data = xlrd.open_workbook('stocknum.xlsx')
    sheet = data.sheets()[3]
    nrows =  sheet.nrows
    for i in xrange(nrows):
         stock = sheet.cell(i, 0).value
         tmp_split = stock.split('.')
         if tmp_split:
             stock_num = tmp_split[0]
             Stock_queue.put(stock_num)

def print_data():

    get_stock_num()
    while Stock_queue.qsize() > 0:
        stock_num = Stock_queue.get()
        get_html_data(stock_num)

def main():
    get_stock_num()
    # print Stock_queue.qsize()
    # work_manager = WorkManager()
    work_manager = WorkManager(Stock_queue.qsize(), max_threads)
    work_manager.finish_all_threads()

    print Html_queue.qsize()
    stock_nums = Html_queue.qsize()
    total_nums = 0
    while not Html_queue.empty():
        total_nums += Html_queue.get()
    # for item in xrange(stock_nums):
        # total_nums += item
    print 'total posts:', total_nums

if __name__ == '__main__':
    os.system('printf "\033c"')

    # main()
    print_data()
