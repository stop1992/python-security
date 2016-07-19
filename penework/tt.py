#encoding:utf-8

import os

from setEnvironment import setEnv
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from Queue import Queue

def main():

    in_queue = Queue()
    a = 10


    def test():
        for i in xrange(10):
            in_queue.put('test')
        a = 1

    test()

    print in_queue.qsize()
    print a


    # logger.log(CUSTOM_LOGGING.SYSINFO, 'this is a test')


if __name__ == '__main__':
    os.system('clear')

    main()


