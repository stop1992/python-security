#!/usr/bin/env python
# encoding: utf-8

import os
import re
import time

def get_file_name(pre_name, count):
    if len(count) == 1:
        return pre_name + '_' + '0' + count + '.txt'
    else:
        return pre_name + '_' + count + '.txt'

def start_crawler(pre_direc, count):
    directory = 'stocknum_02'
    file_name = get_file_name(directory, str(count))
    file_name = directory + '\\' + file_name
    old_file = open('spider.py', 'r')
    codes = old_file.readlines()
    codes_len = len(codes)
    pattern = re.compile(r'stocknum_(\d+)\\stocknum_(\d+)_(\d+).txt')
    j = 0
    for code in codes:
        find = pattern.search(code)
        result = pattern.sub(file_name, code)
        if result and find:
            codes[j] = result
            # print result
            print 'find and replace, so handle', file_name, '........\n'
        j += 1
    new_file = open('spider.py', 'w')
    for line in codes:
        new_file.write(line)
    new_file.close()
    os.system('start ' + 'C:\\Python27\\Scripts\\' + 'scrapy crawl guba')

def check_scrapy():
    while True:
        fp = os.popen('tasklist')
        # print type(fp)
        pattern = re.compile('scrapy.exe')
        sign = False
        for line in fp:
            find = pattern.search(line)
            if find:
                sign = True
                print 'scrapy.exe is running, so sleep 120s...'
                time.sleep(120)
        if sign == False:
            print 'scrapy isn\'t running..., so start new scrapys...'
            break

def modify_files():
    file_nums = 5
    count = 1
    for name in xrange(file_nums):
        pre_direc = "E:\\scrapy\\guba_distribute_crawler"
        start_crawler(count)
        count += 1

        start_crawler(count)
        count += 1

        start_crawler(count)
        count += 1

        start_crawler(count)
        count += 1

        check_scrapy()

if __name__ == '__main__':
    # os.system('printf "\033c"')
    os.system('color 02')

    modify_files()
