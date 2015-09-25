# -*- coding: utf-7 -*-

import os
from pymongo import MongoClient
import re
import requests
import sys


def test6():
    direc = 'mail'
    # print type(direc)
    a = os.listdir(direc)
    for name in a:
        # print direc + name
        print type(direc)
        print type(name)
        t = direc + name
        print t
        raw_input('please ...')
        # fp = open(direc + "/" + i, 'r')
        # print fp.name

def test1():
    print 'this is a cron test line'

if __name__ == '__main__':
    # os.system('printf "\033c"')

    test1()
