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
from Queue import Queue

# from test_result import TestResult

site_total = 0


# class SiteCrawler(object):


site = 'http://bbs.browser.qq.com'
imag_tag_urls = set()
a_tag_urls = set()
a_tag_urls.add(site)


# parent_depth = 0
crawl_depth = 5


# visite = set()
visited = set()
visite_queue = Queue()

def bread_crawl():
    url = site
    visited.add(url)
    visite_queue.put(url)

    while crawl_depth <= current_depth:

        links = []

        while visite_queue.qsize() > 0:
            url = visite_queue.get()
            link = crawler(url, parent_depth)
            for i in link:
                links.append(i)





def crawler(url, parent_depth):

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.useragent"] = (user_agent)
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.get(url)

    # print 'getting img tag url...'
    for img in driver.find_elements_by_tag_name('img'):
        imag_tag_urls.add(img.get_attribute('src'))

    # print 'get a tag url...'
    for a in driver.find_elements_by_tag_name('a'):
        href = img.get_attribute('href')
        if 'http' in href:
            a_tag_urls.add(href)
            visite_queue.put(href)
    depth = parent_depth + 1

    driver.quit()



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
