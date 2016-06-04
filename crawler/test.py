#!/usr/bin/env python
# encoding: utf-8

import subprocess
import os
import requests

# from multiprocessing import Pool, Queue
# from Queue import Queue as Queue_Queue

from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

# queue = Queue()


def func(n):
    print n

    for i in xrange(100):
        requests.get('http://www.baidu.com')
        print 'get success...'

def main():

    pool = Pool()
    # for i in xrange(3):
    pool.map(func, xrange(3))

        # pool.apply_async(test, args=(i,))
    # pool.close()
    # pool.join()

    # print queue.qsize()


if __name__ == '__main__':
    os.system('clear')

    main()
