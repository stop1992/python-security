# encoding:utf-8

import requests
import os
import re
from bs4 import BeautifulSoup
import urllib
import urllib2
import cookielib
from selenium import webdriver
import time
import pdb

try:
    import cPickle as pickle
except:
    import pickle

class ZoomEye(object):
    def __init__(self):

        Host = 'www.zoomeye.org'
        User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0'
        Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        Accept_Language = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        Accept_Encoding = 'gzip, deflate'
        DNT= 1
        Connection= 'keep-alive'

        self.headers = {
                'Host':Host,
                'User-Agent':User_Agent,
                'Accept':Accept,
                'Accept-Language':Accept_Language,
                'Accept-Encoding': Accept_Encoding,
                'DNT':1,
                'Connection':Connection
                }
        self.fp = open('relative_sites.txt', 'w')
        self.fp.close()

    def get_site(self):

        service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=https'
            ]

        self.driver = webdriver.PhantomJS(service_args=service_args)

        # fist step, get cookie by request url
        url = 'https://www.zoomeye.org'
        self.driver.get(url)
        self.driver.refresh()

    def write_results2file(self):

        ul_element = self.driver.find_elements_by_css_selector('.result.web')[0]
        a_elements = ul_element.find_elements_by_css_selector('h3>a')

        self.fp = open('relative_sites.txt', 'a+')

        for a in a_elements:
            href = a.get_attribute('href')
            print 'get ' + href
            self.fp.write(href + '\n')

        self.fp.close()


    def get_result(self):

        self.get_site()

        print '-' * 80
        print 'getting page 1....'
        search_dork = 'https://www.zoomeye.org/search?q=app%3Adiscuz%20php%3A%225.5.7%22&p=1&t=web'
        self.driver.get(search_dork)
        self.write_results2file()

        result_summary = self.driver.find_elements_by_class_name('result-summary')[0]
        result_counts = int(result_summary.text.split()[2])
        if result_counts%10:
            pages = result_counts / 10 + 1
        else:
            pages = result_counts / 10

        for page in xrange(2, pages+1):
            print '-' * 70
            print 'getting page ', page, '.....'
            search_dork = 'https://www.zoomeye.org/search?q=app%3Adiscuz%20php%3A%225.5.7%22&p=' + str(page) + '&t=web'
            self.driver.get(search_dork)
            self.write_results2file()
            time.sleep(3)

        driver.quit()


def main():
    zoom = ZoomEye()
    zoom.get_result()

if __name__ == '__main__':
    os.system('clear')

    main()
