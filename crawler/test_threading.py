# encoding:utf-8

import os
import threading
import Queue
from multiprocessing import Queue as mpqueue


# queue = Queue.Queue()
queue = mpqueue()

class Test(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)

        self.start()

    def run(self):

        for i in xrange(1000000):
            queue.put('test')


if __name__ == '__main__':

    os.system('clear')

    t1 = Test()
    t2 = Test()
    t1.join()
    t2.join()

    print queue.qsize()
