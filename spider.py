# encoding:utf-8

import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import sys
from bs4 import BeautifulSoup
import codecs
import urlparse

# from test_result import TestResult

site_total = 0


class SiteCrawler(object):

    def __init__(self):

        self.site = 'http://bbs.browser.qq.com'
        self.imag_tag_urls = set()
        self.a_tag_urls = set()
        self.a_tag_urls.add(self.site)

    def handle(self):
        _crawler(

    def _crawler(self, url):

        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.useragent"] = (self.user_agent)
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.get(url)

        print 'getting img tag url...'
        for img in self.driver.find_elements_by_tag_name('img'):
            self.imag_tag_urls.add(img.get_attribute('src'))

        print 'get a tag url...'
        for a in self.driver.find_elements_by_tag_name('a'):
            href = img.get_attribute('href')
            if 'http' in href:
                self.a_tag_urls.add(href)

        self.driver.quit()

def main():

    try:
        sitecrawler = SiteCrawler()
        sitecrawler.crawler()

    except KeyboardInterrupt:
        print 'press keyboardinterrupt, so quit....'
        google.driver.quit()


if __name__ == '__main__':
    os.system('clear')

    main()
