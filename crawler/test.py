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

def add_ch(ch):
    return ch+'abc'

def test():
    ch = ['a\r\n', 'b\n\r']
    t = map(strip, ch)

    print t



if __name__ == '__main__':
    os.system('printf "\033c"')

    test()
