# encoding:utf-8


import os
import threading
from multiprocessing import Pool, Queue


queue = Queue()

class WorkManager(object):

    # def __init__(self, thread_pool_size, lock):
    def __init__(self, thread_pool_size):

        self.thread_pool = [] # initiate, no have a thread # self.lock = lock self.thread_pool_size = thread_pool_size
        self.__init_thread_pool()

    def __init_thread_pool(self):
        # for i in xrange(self.thread_pool_size):
        # self.thread_pool.append(WorkThread('1111111111\n', self.lock))
        self.thread_pool.append(WorkThread('1111111111\n'))
        # self.thread_pool.append(WorkThread('2222222222\n', self.lock))
        self.thread_pool.append(WorkThread('2222222222\n'))

    def finish_all_threads(self):
        for i in xrange(self.thread_pool_size):
            if self.thread_pool[i].is_alive():
                self.thread_pool[i].join()


class WorkThread(threading.Thread):

    # def __init__(self, slogan, lock):
    def __init__(self, slogan):
        threading.Thread.__init__(self)
        # self.man = Man()
        # self.fp = fp
        # self.lock = lock
        self.slogan = slogan
        print 'start thread...'
        self.start()

    def run(self):

        global queue
        for i in xrange(100000):
            # self.lock.acquire()
            queue.put(self.slogan)
            queue.put(self.slogan)
            # self.fp.write(self.slogan)
            # self.fp.write(self.slogan)
            # self.lock.release()
            # print '.'
        # return


# lock = threading.Lock()


def test():
    fp = open('test.txt', 'w')
    t1 = WorkThread(fp, '111111111111111\n')
    t2 = WorkThread(fp, '222222222222222\n')

    t1.join()
    t2.join()

    fp.close()

    for i in open('test.txt', 'r'):
        print i

# def handle(name, lock):
def handle(name):

    print name
    # workmanager = WorkManager(2, lock)
    workmanager = WorkManager(2)
    # print 'test'
    # workmanager = WorkManager(2)
    workmanager.finish_all_threads()

def main():

    pools = Pool()

    # fp = open('test.txt', 'w')

    for i in xrange(3):
        # pools.apply_async(handle, args=('processing '+str(i), threading.Lock()))
        pools.apply_async(handle, args=('processing '+str(i), ))

    pools.close()
    pools.join()

    global queue
    print 'quseize:' , queue.qsize()
    # raw_input('wait...')
    fp = open('test.txt', 'w')
    print '-------------------'
    while queue.qsize() > 0:
        tmp = queue.get()
        # print tmp
        fp.write(tmp)
    fp.close()


if __name__ == '__main__':
    os.system('clear')

    main()
