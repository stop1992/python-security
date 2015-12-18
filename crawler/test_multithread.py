# encoding:utf-8


import os
from multiprocessing import Pool, Queue, Process, Lock
from gevent.pool import Pool as ge_pool
from gevent.queue import Queue as ge_queue
from Queue import Queue as q_Queue
import time

# from file_lock import FileLock

queue = Queue()
result = Queue()
# queue = ge_queue()
# queue = q_Queue()

# fp = open('test.txt', 'w')
# flock = FileLock(fp)

NUMS = 5
# complete = [False] * NUMS

# def handle(slogan, queue):
# lock = Lock()
# fp = open('test.txt', 'w')

def handle(i):

    # print 'test'
    # print i

    # for i in xrange(1000000):
    for j in xrange(10000000):
        queue.put('test\n')
        # print 'put...'
        # queue.put(slogan)
    # queue.put('DONE')
    # global complete
    # complete[i] = True
    # print i, complete[i]
    result.put('DONE')
    print 'put done'
    # queue.put(-1)
    # queue.cancle_join_thread()
    # print queue.qsize()

    # for i in xrange(10000):
        # queue.get()
        # lock.acquire()
        # fp.write(queue.get())
        # lock.release()

def check():

    while True:


        if result.qsize() == NUMS:
            break
        else:
            time.sleep(2)
        # data = queue.get()

        # if data == 'DONE':
        # if queue.qsize() == 1001:
            # break
        # else:
            # print 'wait 1s'
            # time.sleep(1)

    print 'put all done'

def main():

    pools = Pool(2)
    # pools = ge_pool(2)
    # pools.map(handle, xrange(0, 3))
    for i in xrange(NUMS):
        # pools.apply_async(handle, args=(str(i)*5+'\n', queue))
        pools.apply_async(handle, args=(i,))

    check()
    # print 'all put done'

    print queue.qsize()
    # p.join()
    # fp.close()

    # fp = open('text.txt', 'w')
    # while queue.qsize() > 0:
        # fp.write(queue.get())
    # fp.close()


if __name__ == '__main__':
    os.system('clear')

    main()
