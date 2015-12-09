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

def tt():
    fp = open('result.txt', 'a+')
    for i in xrange(10):
        fp.write('this is a test' + '\n')
    fp.write('\n')
    fp.close()

def read_file():
    fp = open('result.txt', 'r')
    print fp.readlines()
    fp.close()

if __name__ == '__main__':
    os.system('printf "\033c"')

    tt()
    read_file()
