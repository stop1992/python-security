# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient
import re
import requests
import sys
import random
import string
from PIL import Image
import pytesseract

from multiprocessing import Queue
from multiprocessing import Pool

import gevent
from gevent import monkey
monkey.patch_socket()
from gevent.pool import Pool

queue = Queue()

def add_ch():
    for i in xrange(10000):
        queue.put(i)

def handle(name):
    while queue.qsize() > 0:
        print name
        queue.get()
        print queue.qsize()
    return

def main():

    add_ch()
    print 'qsize:', queue.qsize()

    pools = Pool()
    for i in xrange(3):
        pools.apply_async(handle, args=('processing '+str(i), ))

    pools.close()
    pools.join()

    print 'done'
    print 'done'
    print 'done'

def handle2(i):

    print i

    for i in xrange(10):
        requests.get('http://www.zhihu.com')


def main2():

    pools = Pool(20)
    pools.map(handle2, xrange(100))

if __name__ == '__main__':
    os.system('clear')

    main2()
