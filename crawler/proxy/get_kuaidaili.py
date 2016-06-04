#!/usr/bin/env python
# encoding: utf-8

import os
import re
import subprocess
import requests
import time
import IPython


from get_curl_header_post import get_curl_header_post

class Proxy(object):

    def __init__(self):
        self.proxy_file = open("proxy.txt", 'w')

    def handle_html(self):

        # pattern_ip = re.compile("<td>(\d+\.\d+\.\d+\.\d+)</td>")
        pattern_ip = re.compile("\"IP\">(\d+\.\d+\.\d+\.\d+)</td>")
        # pattern_port = re.compile("<td>(\d+)</td>")
        pattern_port = re.compile("\"PORT\">(\d+)</td>")

        all_ip = pattern_ip.findall(self.response.text)
        all_port = pattern_port.findall(self.response.text)

        # print len(all_ip), len(all_port)
        if len(all_ip) == len(all_port) and len(all_ip) != 0:
            length = len(all_ip)
            for i in xrange(length):
                self.proxy_file.write(all_ip[i] + ':' + all_port[i]+'\n')
            return 'successfully'
        else:
            return 'error'


    def get_proxy(self):

        raw_curl_data = "curl 'http://www.kuaidaili.com/free/inha/1047/' -H 'Pragma: no-cache' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: no-cache' -H 'Referer: http://www.kuaidaili.com/free/inha/1047/' -H 'Cookie: _gat=1; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1463909105; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1463987265; _ga=GA1.2.1243866898.1463909105' -H 'Connection: keep-alive' --compressed"
        header, post_data = get_curl_header_post(raw_curl_data)

        for page in xrange(1, 500):
            url = 'http://www.kuaidaili.com/free/inha/%s/' % page
            self.response = requests.get(url, headers=header)
            # print self.response.text
            sign = self.handle_html()
            print 'get %s %s...' % (url, sign)
            time.sleep(2)

        self.proxy_file.close()


def main():

    proxy = Proxy()
    proxy.get_proxy()


if __name__ == '__main__':
    os.system('clear')

    main()
