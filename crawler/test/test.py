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
import urllib
import urllib2


def check():

    response = requests.get('http://192.168.1.106/test/test.php')
    # print response.content

    pattern = re.compile(ur"HTTP Headers Information|Apache Environment|PHP License")
    if pattern.search(response.content):
        print 'php info success'
    else:
        print 'php info failed'


if __name__ == '__main__':
    os.system('clear')

    check()
