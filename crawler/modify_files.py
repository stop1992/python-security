#!/usr/bin/env python
# encoding: utf-8

import os
import re

def modify_files():
    old_file = open('spider.py', 'r')
    codes = old_file.readlines()
    pattern = re.compile('stocknum_(\d+)_(\d+)')
    for code in codes:
        result = pattern.search(code)
        if result:
            print type(result.group())

if __name__ == '__main__':
    os.system('printf "\033c"')

    modify_files()
