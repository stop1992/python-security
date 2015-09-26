#!/usr/bin/env python
# encoding: utf-8

# this is a template for using multiprocessing and threading
# first, create a pools(including some process), then under every
# process, create some thread to handle something.
# warning: processes don't share memory, but threads do.

import os
import threading
import multiprocessing
import Queue as Queue_Queue
from multiprocessing import Queue, Pool
import traceback

# global variable
max_threads = 5
initial_data_queue = Queue()

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
            self.work_queue.put((handle_func, initial_data_queue.get()))

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
            except Queue_Queue.Empty:
                print 'work_queue is empty...'


def handle_func(data_from_initial_data_queue):
    pass


def initial_queue():
    pass

def handle(process_name):
    """
    warning: the accouts of work_queue must be the same as initial_data_queue
    """
    print process_name, 'is running...'
    work_manager = WorkManager(initial_data_queue.qsize()/3, max_threads)
    work_manager.finish_all_threads()

def main():

    initial_queue()
    pools = multiprocessing.Pool()
    for i in xrange(3):
        pools.apply_async(handle, args=('process_'+str(i),))
    pools.close()
    pools.join()


if __name__ == '__main__':
    os.system('printf "\033c"')

    main()
