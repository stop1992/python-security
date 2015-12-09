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
        # self.url = 'https://www.zoomeye.org/search?q=app%3A%22discuz%22%20php%3A%225.5.7%22&p=6&t=web'


    def get_first_page(self):

        service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=https'
            ]

        driver = webdriver.PhantomJS(service_args=service_args)

        # fist step, get cookie by request url
        url = 'https://www.zoomeye.org'
        driver.get(url)
        driver.refresh()
        # time.sleep(2)
        return driver

    def get_result(self):

        driver = get_first_page()

        print '-' * 80
        search_dork = 'https://www.zoomeye.org/search?q=app%3Adiscuz%20php%3A%225.5.7%22&p=1&t=web'
        driver.get(search_dork)


        driver.quit()


def test_req():

    url = 'http://www.zhihu.com'
    req1 = urllib2.Request(url)
    response = urllib2.urlopen(req1)
    cookie = response.headers.get('Set-Cookie')
    print response.getcode()

    url = 'http://www.zhihu.com'
    req2 = urllib2.Request(url)
    req2.add_header('cookie', cookie)
    response = urllib2.urlopen(req2)
    print response.getcode()

    # url = 'https://www.zoomeye.org'
    # response = urllib2.urlopen(url).read()
    # print response

def main():
    zoom = ZoomEye()
    # zoom.get_html()
    # zoom.get_html_req()
    zoom.get_html_driver()
    # test_req()

if __name__ == '__main__':
    os.system('clear')

    main()
