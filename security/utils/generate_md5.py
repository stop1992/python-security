#!/usr/bin/env python
# encoding: utf-8

import os
import hashlib

def generate_md5():
    init_strings = ['daitao', 'wangxi', 'abcde', 'admin', 'passowrd', 'big', 'small']
    m = hashlib.md5()
    fp = open('md5.txt', 'w')
    for string in init_strings:
        m.update(string)
        fp.write(m.hexdigest()+'\n')
    fp.close()
    for i in open('md5.txt', 'r'):
        print i

def generate_single():
    m = hashlib.md5()
    m.update('daitaocaiguai')
    print m.hexdigest()

if __name__ == '__main__':
    os.system('printf "\033c"')

    generate_single()
