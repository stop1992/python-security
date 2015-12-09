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


def add_small():
    tmp_txt = open('result.txt', 'r').readlines()
    fp = open('tmp.txt', 'w')
    start = 0
    for i in xrange(0, len(tmp_txt)):
        if i % 2 == 0:
            fp.write('>' + tmp_txt[i])
        else:
            fp.write(tmp_txt[i])
    fp.close()

if __name__ == '__main__':
    os.system('printf "\033c"')

    add_small()

