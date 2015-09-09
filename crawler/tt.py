#!/usr/bin/env python
# encoding: utf-8

import os
import threading
from Queue import Queue
from multiprocessing import Process, Pool

# global variable
max_threads = 11
Stock_queue = Queue()
COUNT = 0

class WorkManager:
    def __init__(self, work_queue_size=1, thread_pool_size=1):
        self.work_queue = Queue()
        self.thread_pool = [] # initiate, no have a thread
        self.work_queue_size = work_queue_size
        self.thread_pool_size = thread_pool_size
        self.__init_work_queue()
        self.__init_thread_pool()

    def __init_work_queue(self):
        for i in xrange(self.work_queue_size):
            self.work_queue.put((func_test, Stock_queue.get()))

    def __init_thread_pool(self):
        for i in xrange(self.thread_pool_size):
            self.thread_pool.append(WorkThread(self.work_queue))

    def finish_all_threads(self):
        for i in xrange(self.thread_pool_size):
            if self.thread_pool[i].is_alive():
                self.thread_pool[i].join()

class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while self.work_queue.qsize() > 0:
            try:
                func, args = self.work_queue.get(block=False)
                func(args)
            except Queue.Empty:
                print 'queue is empty....'

def handle(process_name):
    print process_name, 'is running...'
    work_manager = WorkManager(Stock_queue.qsize()/3, max_threads)
    work_manager.finish_all_threads()

def func_test(num):
    global COUNT
    COUNT += num

def prepare():
    for i in xrange(50):
        Stock_queue.put(i)

def main():

    prepare()
    pools = Pool()
    for i in xrange(3):
        pools.apply_async(handle, args=('process_'+str(i),))
    pools.close()
    pools.join()

    global COUNT
    print 'COUNT: ', COUNT


if __name__ == '__main__':
    os.system('printf "\033c"')

    main()
