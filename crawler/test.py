#-*- encoding:utf-8 -*-

import xlrd
import os
import requests
from collections import defaultdict
from selenium import webdriver
import types
import re
from redis import Redis
from pymongo import MongoClient
import time
import threading
# from Queue import Queue
import Queue
import pdb
import xlwt

def test15():
    server = MongoClient('localhost', 27017)
    db = server.guba_data
    lack_queue = Queue.Queue()
    line_num = 1
    for stock_num in open('stocknums.txt', 'r'):
        stocknum = 'db' + stock_num.strip()
        collec = db[stocknum]
        if collec.count() == 0:
            print stock_num.strip(), 'is not exist'
            lack_queue.put(stock_num)
            # print line_num
        line_num += 1

    print lack_queue.qsize()


def test14():
    server = MongoClient('localhost', 27018)
    db = server.guba
    lack_queue = Queue.Queue()
    line_num = 1
    for stock_num in open('stocknums.txt', 'r'):
        stocknum = 'db' + stock_num.strip()
        collec = db[stocknum]
        # print collec.count()
        if collec.count() == 0:
            print stock_num.strip(), 'is not exist'
            lack_queue.put(stock_num)
            # print line_num
        line_num += 1

    print lack_queue.qsize()


def test16():
    host = '192.168.1.108'
    port = 27018
    client = MongoClient(host, port)
    db = client.guba

    col = db['db000002']
    a = col.find()
    pdb.set_trace()
    for i in a:
        # pdb.set_trace()
        print type(i)
        # raw_input('please')

def test17():
    work = xlwt.Workbook()
    sheet = work.add_sheet('test')
    for i in xrange(300):
        sheet.write(0, i, 'test')
    work.save('test.xls')


log_file = open('test_log.txt', 'w')
lock = threading.Lock()

def test1(i):
    print 'this is thread_' , i
    global lock, log_file
    lock.acquire()
    # tmp = 0
    # for j in xrange(100000):
        # tmp += j
    log_file.write('\n-----------------------------------------------\n')
    log_file.write('this is thread_' + i + ' is running....' + '\n')
    log_file.write('this is thread_' + i + ' is running....' + '\n')
    log_file.write('this is thread_' + i + ' is running....' + '\n')
    log_file.write('this is thread_' + i + ' is running....' + '\n')
    log_file.write('this is thread_' + i + ' is running....' + '\n')
    log_file.write('-----------------------------------------------\n')
    lock.release()

def test2():
    for i in xrange(1000):
        new_thread = threading.Thread(target=test1, args=(str(i),))
        new_thread.start()


if __name__ == '__main__':
    os.system('printf "\033c"')

    test2()
