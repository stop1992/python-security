#encoding:utf-8

import re
import requests
import sys
import os
import threading
import time
from Queue import Queue

from utils.randomuseragent import randomuseragent

from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.exception import PocsuiteThreadException


class Activemq(object):

    def __init__(self):
        pass

    def check_cve_2016_3088(self, url):
        '''
        affected version:
        Apache ActiveMQ 5.0.0 - 5.13.2
        '''

        requests = requests.Session()
        url = 'http://192.168.1.101:8161'
        headers = {
                "Authorization": "Basic YWRtaW46YWRtaW4=",
                "User-Agent": randomuseragent('useragents.txt')
                }
        response = requests.get(url, headers=headers, timeout=5)
        # print response.text
        print response.status_code


    def run(self):

        threads = []
        thread_nums = 20

        try:
            for thread_num in xrange(thread_nums):
                thread = threading.Thread(target=check_cve_2016_3088, name=str(thread_num))
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
    activemq.check_cve_2016_3088('ll')



if __name__ == '__main__':
    os.system('clear')

    main()
