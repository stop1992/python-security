#!/usr/bin/env python
# encoding: utf-8

import multiprocessing
import os
from

class Test(multiprocessing.Process):
    def run(name):
        print 'processing.....'
        tmp = 0
        for i in xrange(10000000):
            tmp += i
        print 'process done'

if __name__ == '__main__':
    os.system('printf "\033c"')

    t = Test()
    pools = multiprocessing.Pool()
    jobs = []
    for i in xrange(4):
        t = Test()
        jobs.append(t)
        t.start()
    # print jobs
    print 'all jobs done'
