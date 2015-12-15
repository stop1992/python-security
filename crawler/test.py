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
import sys
from gevent.pool import Pool
import codecs


def test(i):
    fp = codecs.open('200.txt', 'a+', 'utf-8')
    for i in xrange(10):
        fp.write('this is a test')
        print 'done'
    fp.close()

if __name__ == '__main__':
    os.system('printf "\033c"')

    # test()

    pools = Pool(3)
    pools.map(test, xrange(1000))
    print codecs.open('200.txt', 'r', 'utf-8').readlines()
