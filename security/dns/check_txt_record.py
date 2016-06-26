#!/usr/bin/env python
# encoding: utf-8

import requests
import os
import codecs
import re
import time
import subprocess

from get_curl_header_post import get_curl_header_post

class Sites(object):

    def __init__(self):
        self.sites_file = open('top_sites.txt', 'w')
        self.pattern = re.compile("href=\"\/siteinfo\/(\S+)\">")

    def pages(self):

        # get top 500
        for i in xrange(20):
            # url = 'http://www.alexa.com/topsites/countries;%s/US' % str(i)
            url = 'http://www.alexa.com/topsites/countries;%s/CN' % str(i)
            print 'getting %s' % url
            self.get_top_sites(url)
            time.sleep(5)

        self.sites_file.close()


    def get_txt_record(self):

        record_fp = open('txt_recorder.txt', 'w')
        total_no_record = 0


        # for s in open('top.txt', 'r'):
        for s in open('top_sites.txt', 'r'):
            host_sub = subprocess.Popen(['host', '-t', 'txt', s.strip()], stdout=subprocess.PIPE)
            host_out = host_sub.stdout.readlines()
            for b in host_out:
                if 'no TXT record' in b:
                    print b.strip()
                    record_fp.write(b)
                    total_no_record += 1
        print '[*] total_no_record: ', total_no_record

        record_fp.close()



    def get_top_sites(self, url):

        # raw_curl = "curl 'http://www.alexa.com/topsites/countries;2/CN' -H 'Pragma: no-cache' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: no-cache' -H 'Referer: http://www.alexa.com/topsites/countries;1/CN' -H 'Cookie: rpt=%21; rpt=%21; lv=1465290116; _alx_as=%7B%22status%22%3A0%7D; __asc=2a4ddd181552a114b5d19855a4c; __auc=2a4ddd181552a114b5d19855a4c' -H 'Connection: keep-alive' --compressed"

        # headers, post = get_curl_header_post(raw_curl)

        response = requests.get(url)
        result_sites = self.pattern.findall(response.text)
        for s in result_sites:
            print '--' + s
            self.sites_file.write(s + '\n')


def main():
    site = Sites()
    site.pages()
    site.get_txt_record()
    # get_top_sites()


if __name__ == '__main__':
    # os.system('clear')

    main()
