# encoding:utf-8

import os
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import sys
from bs4 import BeautifulSoup
import urlparse
from Queue import Queue
from splinter import Browser



site_total = 0


class Spider(object):

    def __init__(self):

        self.site = 'http://bbs.browser.qq.com'
        # self.site = 'http://www.baidu.com'
        self.netloc = '.'.join(urlparse.urlparse(self.site).netloc.split('.')[1:])
        # print self.netloc
        # raw_input('wait...')
        # self.imag_tag_urls = set()

        self.crawl_depth = 5

        self.visited = set()
        self.visite_queue = Queue()
        self.visite_queue.put(self.site)


    def breadth_crawler(self):
        current_depth = 0

        while self.crawl_depth >= current_depth:

            links = []
            while self.visite_queue.qsize() > 0:
                url = self.visite_queue.get()
                link = self._crawl(url)
                for i in link:
                    links.append(i)

            for j in links:
                if j not in self.visited:
                    self.visite_queue.put(j)

            current_depth += 1
            print current_depth


    def _crawl(self, url):

        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
        self.browser = Browser(driver_name='phantomjs', user_agent=user_agent)

        try:
            out_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print "[{out_time}] crawling {url}".format(out_time=out_time, url=url)
            self.browser.visit(url)
            self.visited.add(url)
        except Exception, e:
            print e

        link = []
        soup = BeautifulSoup(self.browser.html, 'lxml')
        for a in soup.find_all('a'):
            href = a.get('href')
            # print href
            if href:
                url_netloc = '.'.join(urlparse.urlparse(href).netloc.split('.')[1:])
                if url_netloc == self.netloc and ('http' in href or 'https' in href):
                    link.append(href)

        return link


def main():

    try:
        spider = Spider()
        spider.breadth_crawler()

    except KeyboardInterrupt:
        print 'press keyboardinterrupt, so quit....'
        # spider.driver.quit()


if __name__ == '__main__':
    os.system('clear')

    main()
