#!/usr/bin/env python
# encoding: utf-8

from multiprocessing import Process
from multiprocessing import Pool
import os

def run_proc(name):
    tmp = 0
    for i in xrange(100000000000):
        tmp += i
    print 'Run child process %s (%s)....' % (name, os.getpid())

def test():
    p = Process(target=run_proc, args=('test', ))
    print 'child process will start'
    p.start()
    tmp = 0
    for i in xrange(1000000000000):
        tmp += i
    p.join()
    print 'process all end'

def test2():
    pools = Pool(4)
    for i in xrange(4):
        pools.apply_async(run_proc, ('test',))
    print 'Waiting for all subprocesses done...'
    pools.close()
    pools.join()
    print 'all subprocess done'

if __name__ == '__main__':
    os.system('printf "\033c"')

    test2()
