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


def main():

    a = 0

    while True:

        if a < 0:
            break





def main2():

    pools = Pool(20)
    pools.map(handle2, xrange(100))

if __name__ == '__main__':
    os.system('clear')

    main2()
