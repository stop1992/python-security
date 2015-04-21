#!/usr/bin/env python

import re
import os

if __name__ == '__main__':
    # f = open('who.txt', 'r')
    f = os.popen('who', 'r')
    for eachLine in f.readlines():
        print re.split(r'\s\s+|\t', eachLine.strip())
    f.close()
