#!/usr/bin/env python
# encoding: utf-8

import os
import requests
import copy
from bs4 import BeautifulSoup
import IPython
import re
import subprocess


from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import DesiredCapabilities
from seleniumrequests import PhantomJS
from seleniumrequests import Firefox
from get_curl_header_post import get_curl_header_post

import codecs


class Getproxy(object):

    def __init__(self):

        self.proxy_file = open('proxy.txt', 'w')


    def test_proxy(self):
        pass

    def handle_html(self):

        # print self.response.text
        pattern_ip = re.compile("IPDecode\(\"(\S+)\"\)")
        pattern_port = re.compile("\"center\"\>(\d+)\<\/td")
        all_ip = pattern_ip.findall(self.response.text)
        all_port = pattern_port.findall(self.response.text)

        if all_ip != 50:
            print 'please update raw_curl_data ...'
            print 'get proxy error, so exit ...'
            os._exit(1)

        # ip_file_name = '/home/xinali/python/crawler/ip.txt'
        ip_file_name = '/home/xinali/python/crawler/ip.txt'

        ip_file = open(ip_file_name, 'w')
        for ip in all_ip:
            ip_file.write(ip+'\n')
        ip_file.close()

        # result_out = subprocess.Popen(["node", "/home/xinali/python/crawler/get_ip.js", ip_file_name], stdout=subprocess.PIPE)
        result_out = subprocess.Popen(["node", "get_ip.js", ip_file_name], stdout=subprocess.PIPE)
        ip_readlines = result_out.stdout.readlines()

        i = 0
        for ip in ip_readlines:
            extract_ip = re.search(">(\S+)<", ip)
            if extract_ip:
                self.proxy_file.write(extract_ip.groups(0)[0] + ' ' + all_port[i] + '\n')
                i += 1


    def get_proxy(self):

        raw_curl_data = "

        headers, post_data = get_curl_header_post(raw_curl_data)
        # html_content = codecs.open('html_content.html', 'w', 'utf-8')
        html_content = codecs.open('html_content.txt', 'wb', 'utf-8')

        for page in xrange(1, 25):
            url = 'http://www.freeproxylists.net/zh/?page=%s' % (str(page))
            self.response = requests.get(url, headers=headers)
            self.handle_html()
            print 'getting page %d successfully...' % page

        self.proxy_file.close()


    def handle_by_phantomjs(self):

        headers, post_data = get_curl_header_post(raw_curl_data)
        self.cookie_dict = {}
        user_agent = ''

        del_key = ''
        for key in headers:
            if key == 'User-Agent':
                # dcap["phantomjs.page.settings.userAgent"] = headers[key]
                # webdriver.DesiredCapabilities.PHANTOMJS["phantomjs.page.settings.userAgent"] = headers[key]
                del_key = key
            elif key == 'Cookie':
                cookies = headers[key].split(';')
                for cookie in cookies:
                    cookie = cookie.split('=')
                    cookie_key = cookie[0].strip()
                    cookie_value = cookie[1].strip()
                    self.cookie_dict[cookie_key] = cookie_value

        user_agent = headers[del_key]

        # dele user-agent, user-agent in settings
        del headers[del_key]

        # driver_phantomjs = webdriver.Remote(command_executor='http://127.0.0.1:8910', # desired_capabilities=DesiredCapabilities.PHANTOMJS) desired_capabilities=dcap)

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        for key, value in headers.iteritems():
            # print key, value
            dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
        dcap["phantomjs.page.settings.userAgent"] = user_agent

        print '\n\ntotal need data:'
        for key, word in dcap.iteritems():
            print key, word
        print '#'*100
        raw_input('wait total data...')

        self.driver_phantomjs = webdriver.PhantomJS(desired_capabilities=dcap)

        url = 'https://www.baidu.com'

        self.driver_phantomjs.get(url)
        # self.driver_phantomjs.delete_all_cookies()
        self.driver_phantomjs.add_cookie(self.cookie_dict)
        self.handle_by_phantomjs()

        for page in xrange(1, 20):

            url = 'http://www.freeproxylists.net/zh/?page=%s' % (str(page))
            try:

                self.driver_phantomjs.get(url)
                print self.driver_phantomjs.page_source
            except Exception, e:
                self.driver_phantomjs.get_screenshot_as_png('error.png')
                print 'get error png successfully'
            print '*' * 100
            for  key, word in self.driver_phantomjs.desired_capabilities.iteritems():
                print key, word

            # response = driver.request('POST', url, headers=headers, data=post_data, page_load_timeout=5)
            raw_input('wait....')


def main():

    getproxy = Getproxy()
    # getproxy.handle_html()
    getproxy.get_proxy()


if __name__ == '__main__':

    os.system('clear')

    main()
