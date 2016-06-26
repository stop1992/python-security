#!/usr/bin/env python
# encoding: utf-8

import requests
import os
import codecs
import re
import time
import subprocess

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


    def get_top_sites(self, url):

        response = requests.get(url)
        result_sites = self.pattern.findall(response.text)
        for s in result_sites:
            print '--' + s
            self.sites_file.write(s + '\n')


def main():
    site = Sites()
    site.pages()


if __name__ == '__main__':
    # os.system('clear')

    main()
