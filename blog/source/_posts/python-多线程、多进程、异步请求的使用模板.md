---
title: python 多线程、多进程、异步请求的使用模板
categories: Technology
tags: python
---

# python 多线程、多进程、异步请求的使用模板

有时在网络条件很好，抓取数据的服务器对抓取的速度没有任何的限制的情况下，我们会考虑使用多线程，多进程或是异步请求。利用这几种方式抓取数据，我都用过，下面就说一下，我所处理中使用到的模板

## 多线程
多线程使用模板
```python
import os
import threading
from Queue import Queue

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


def handle_func(para):
    // do something

def main():
    
    workmanager = WorkManager(n, m) // n 为线程池的数目，m为工作队列大小
    workmanager.finish_all_threads()
    
if __name__ == '__main__':
    main()
```

## 多进程
多进程使用模板
```python
from multiprocessing import Pool

def func():
    // do something
    
def main():
    pool = Pool() 
    for i in xrange(n): // n 进程池的数目
        pool.apply_async(func, args(...,)) //使用中，参数必须要有，没有的话，传递
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
```
**进程之间的数据是不共享的，如果想所有进程都能处理共同的数据，那么需要使用multiprocessing自己封装的Queue**

## 多进程与多线程
多进程与多线程混合使用模板

> 在实际的使用过程中，该方法的速度并没有想象中的那么快，甚至比接下来要使用的gevent还要慢，我想可能的原因是上下文环境的不断切换，具体原因，作为很菜的自己，没有搞明白

```python
# this is a template for using multiprocessing and threading
# first, create a pools(including some process), then under every
# process, create some thread to handle something.
# warning: processes don't share memory, but threads do.

import os
import threading
import multiprocessing
import Queue as Queue_Queue
from multiprocessing import Queue, Pool

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
    // do something

def initial_queue():
    // do initiate 

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
    main()
```

## 异步请求
gevent最简单的使用方式
```python
import gevent

def func1():
    // do something

def func2():
    // do something

gevent.joinall([
    gevent.spawn(func1),
    gevent.spawn(func2),
])
```

异步的使用和多线程和多进程一样或者说相似，都有一个池的概念，以便控制并发数
最基本的使用方式：
```python
import gevent
from gevent.pool import Pool

pool = Pool(2)

def func(n):
    // do something

pool.map(func, iterable_n)
```
在使用的过程中，有时我们需要所有池处理的结果，并不是每个函数都是单独处理的，这样的话就会涉及到一个问题，异步写数据的安全，为此gevent封装了queue给我们用

```python
import gevent
from gevent.queue import Queue
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

INPUT_QUEUE = Queue()
OUTPUT_QUEUE = Queue()

def pre():
    ...
    INPUT_QUEUE.push()
    ...

def start(n):
    while INPUT_QUEUE.qsize() > 0:
        end(INPUT_QUEUE.get())

def end(para):
    // handle para
    ...
    OUTPUT_QUEUE.push()
    
def main():
    pre()

    pools = Pool(n) // 池的数目
    pools.map(start, iterable_n)

if __name__ == '__main__':
    
    main()
```
