#!/usr/bin/env python

import os
import Queue
import threading
import Queue

thread_queue = Queue.Queue()


class ThreadTest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        thread_queue.put(self)


if __name__ == '__main__':
    os.system('printf "\033c"')

    for i in xrange(5):
        thread = ThreadTest()
        thread.start()

    print thread_queue.qsize()


