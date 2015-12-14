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

def add_ch(ch):
    return ch+'abc'

def test():
    a = 'test'
    if a == 'test':
        print 'so quit'
        sys.exit()
    else:
        print 'not exit'



if __name__ == '__main__':
    os.system('printf "\033c"')

    test()
    print 'after quit'
