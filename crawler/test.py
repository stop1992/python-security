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


def test(i):
   print i

if __name__ == '__main__':
    os.system('printf "\033c"')

    pools = Pool(3)
    pools.map(test, xrange(1000))
