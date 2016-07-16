#!/usr/bin/env python
# encoding: utf-8

import dns.resolver
import os
import sys
sys.path.append('../')
from optparse import OptionParser
from Queue import Queue
import threading
import time
import random


from penework.lib.core.data import logger
from penework.lib.core.enums import CUSTOM_LOGGING
from penework.lib.core.exception import PocsuiteThreadException
from penework.lib.core.threads import runThreads


class SubBrute(object):

    def __init__(self, threads_num, domain):

        self.in_queue = Queue()
        for name in open('names.txt', 'r'):
            name = name.strip() + '.' + domain
            self.in_queue.put(name)

        self.out_queue = Queue()
        self.threads_num = threads_num

        self.nameservers = [
                '223.5.5.5',
                '223.6.6.6',
                '119.29.29.29',
                '114.114.114.114',
                '114.114.115.115',
                '180.76.76.76'
                ]
        self.name_count = 6
        self.reso = dns.resolver.Resolver()
        self.lock = threading.Lock()
        self.found_count = 0

        # count lines of file
        # with open('names.txt') as fp:
            # self.remain_count = sum(1 for x in fp)


    def brute_names(self):

        while self.in_queue.qsize() > 0:
            name = self.in_queue.get()

            # try 5 times for every name
            for _ in xrange(5):

                try:
                    self.reso.nameservers[0] = self.nameservers[random.randrange(self.name_count)]
                    self.reso.lifetime = 10.0
                    ans = self.reso.query(name)
                    ip = ''
                    for rdata in ans:
                        ip += rdata.to_text() + ' '

                    if ip:
                        result = name + '\t' + ip
                        sys.stdout.write('\r' + result + ' ' * 100+ "\n\r")
                        self.out_queue.put(result)

                        self.lock.acquire()
                        self.found_count += 1
                        self.lock.release()
                        break

                except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
                    break

                except Exception, e:
                    pass

            sys.stdout.write('\r' + ' ' * 100 + str(self.found_count) + ' found | '
                            + str(self.in_queue.qsize()) + ' remaining')
            sys.stdout.flush()

    def run(self):

        runThreads(self.threads_num, self.brute_names)

        # threads = []

        # try:
            # for thread_num in xrange(self.threads_num):

                # thread = threading.Thread(target=self.brute_names, name=str(thread_num))
                # thread.setDaemon(True)
                # thread.start()
                # threads.append(thread)

            # alive = True
            # while alive:
                # alive = False

                # for thread in threads:
                    # if thread.isAlive():
                        # alive = True
                        # time.sleep(0.1)

        # except KeyboardInterrupt:

            # if self.threads_num > 1:
                # logger.log(CUSTOM_LOGGING.SYSINFO, "waiting for threads to finish (Ctrl+C was pressed)")

            # try:
                # while (threading.activeCount() > 1):
                    # pass

            # except KeyboardInterrupt:
                # raise PocsuiteThreadException("user aborted (Ctrl+C was pressed multiple times)")


def test():

    parser = OptionParser()
    parser.add_option("-t", "--threads",
                      dest="threads_nums",
                      type="int",
                      help="Number of threads")

    parser.add_option("-d", "--domain",
                      dest="domain",
                      type="string",
                      help="Bruting domain")

    options, args = parser.parse_args()

    if options.threads_nums is None:
        parser.print_help()
        sys.exit()

    if options.domain is None:
        parser.print_help()
        sys.exit()

    subbrute = SubBrute(options.threads_nums, options.domain)
    subbrute.run()


def main():

    # subbrute = SubBrute(options.threads_nums, options.domain)
    threads_num = 10
    domain = 'baidu.com'
    subbrute = SubBrute(threads_nums, domain)
    subbrute.run()



if __name__ == '__main__':
    os.system('clear')

    main()
