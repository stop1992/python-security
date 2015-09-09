#!/usr/bin/env python
# encoding: utf-8

from Queue import Queue
from multiprocessing import Pool#, Queue
import os

queue = Queue()

def func(name):
    for i in xrange(5):
        queue.put(name + '_test_' + str(i))


if __name__ == '__main__':
    os.system('printf "\033c"')

    pools = Pool()
    for i in xrange(3):
        pools.apply_async(func, args=('process_' + str(i), ))
    pools.close()
    pools.join()

    while queue.qsize() > 0:
        print queue.get()
