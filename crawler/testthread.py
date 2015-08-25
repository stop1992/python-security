#!/usr/bin/env python
# encoding: utf-8

import threading
import os

class Test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        print 'this is a test'

class WorkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # self.work_queue = work_queue
        # print self.work_queue.qsize()
        # self.start()
        # print 'after starting'

	def run(self):
            print 'test'
            while True:
                try:
                    func, args = self.work_queue.get(block=False)
                    print args
                    func(args)
                except Queue.Empty:
                    print 'work queue is empty'
                    break
                except requests.ConnectionError:
                    print 'connection error'
                    # while True:
                            # try:
                                    # func(args)
                            # except requests.ConnectionError:
                                    # continue
                    continue



if __name__ == '__main__':
    os.system('printf "\033c"')

    # test = Test()
    work = WorkThread()
    work.start()
