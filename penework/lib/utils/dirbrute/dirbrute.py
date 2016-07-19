#!/usr/bin/env python
# encoding: utf-8

import os
import sys
sys.path.append('../')

from optparse import OptionParser
from Queue import Queue
import threading
import time
import requests


from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.exception import PeneworkThreadException
from thirdparty.termcolor.termcolor import cprint


class DirBrute(object):

    def __init__(self, threads_num, domain):


        self.in_queue = Queue()
        for name in open('dir.txt', 'r'):
            name = domain + name.strip()
            self.in_queue.put(name)

        self.out_queue = Queue()
        self.threads_num = threads_num


        self.lock = threading.Lock()
        self.domain = domain

        # count lines of file
        # with open('names.txt') as fp:
            # self.remain_count = sum(1 for x in fp)


    def brute_names(self):

        while self.in_queue.qsize() > 0:

            try:

                url = self.in_queue.get()
                response = requests.get(url)
                if response.status_code == 200:
                    cprint(url + ' ' + str(response.status_code))
                # else:
                    # cprint(url + ' ' + str(response.status_code), 'red')
                    # sys.stdout.write(url + ' ' + response.status_code)
                # sys.stdout.write('\r' + ' ' * 100 + str(self.found_count) + ' found | ' +
                                 # str(self.in_queue.qsize()) + ' remaining')
                # sys.stdout.flush()
            except Exception, e:
                cprint(e, 'red')


    def run(self):

        threads = []

        try:
            for thread_num in xrange(self.threads_num):

                thread = threading.Thread(target=self.brute_names, name=str(thread_num))
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)

            alive = True
            while alive:
                alive = False

                for thread in threads:
                    if thread.isAlive():
                        alive = True
                        time.sleep(0.1)

        except KeyboardInterrupt:

            if self.threads_num > 1:
                logger.log(CUSTOM_LOGGING.SYSINFO, "waiting for threads to finish (Ctrl+C was pressed)")

            try:
                while (threading.activeCount() > 1):
                    pass

            except KeyboardInterrupt:
                raise PeneworkThreadException("user aborted (Ctrl+C was pressed multiple times)")


def main():

    parser = OptionParser()
    parser.add_option("-t", "--threads",
                      dest="threads_nums",
                      type="int",
                      help="Number of threads")

    parser.add_option("-d", "--domain",
                      dest="domain",
                      type="string",
                      help="Bruting domain, it should like http://example.com")

    options, args = parser.parse_args()

    if options.threads_nums is None:
        parser.print_help()
        sys.exit()

    if options.domain is None:
        parser.print_help()
        sys.exit()

    subbrute = DirBrute(options.threads_nums, options.domain)
    subbrute.run()


if __name__ == '__main__':
    os.system('clear')

    main()
