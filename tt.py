#!/usr/bin/env python
# encoding: utf-8

# import multiprocessing
import os
from pathos import multiprocessing as mp

# def add(x, y):
    # return x + y

class Test():
    def test(self):
        print 'this is a test'

if __name__ == '__main__':
    os.system('printf "\033c"')

    pool = mp.ProcessingPool()
    for i in xrange(3):
        pool
    # print map(add, range(3), range(3))
