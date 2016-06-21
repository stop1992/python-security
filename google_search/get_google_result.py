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

from test_result import TestResult

site_total = 0


class Google(object):

    def __init__(self):

        # self.url = 'https://www.google.com.hk/search?newwindow=1&safe=strict&q=site%3Abaidu.com+intitle%3Apowered+by+discuz&oq=site%3Abaidu.com+intitle%3Apowered+by+discuz&gs_l=serp.3...20457758.20475642.0.20475787.51.41.2.0.0.0.760.7740.2-11j7j2j1j1.22.0....0...1c.1j4.64.serp..27.1.307.0..0.zppyv6hSSsI'
        self.url = 'https://www.google.com.hk/search?q=site%3Aqq.com+intitle%3Apowered+by+discuz&oq=site%3Aqq.com+&aqs=chrome.0.69i59j69i57j69i58j69i60.5382j0j1&{google:bookmarkBarPinned}sourceid=chrome&{google:omniboxStartMarginParameter}ie=UTF-8'
        self.user_agent = 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/47.0.2526.80 safari/537.36'
        codecs.open('google_results.txt', 'w', 'utf-8')
        self.sites = ''

    def handle_captchar_limit(self, url):

        first = True
        while True:
            if 'https://ipv4.google.com/sorry/' in url:
                if first:
                    print 'need captcha....'
                else:
                    print 'captcha error, input captcha again'

                self.driver.get_screenshot_as_file('captcha.png')
                captcha = raw_input('Captcha:')
                self.driver.find_element_by_id('captcha').send_keys(captcha)
                self.driver.find_element_by_name('submit').click()
                url = self.driver.current_url
                first = False
            else:
                break

        if 'repeat the search with the omitted results included' in self.driver.page_source:
            print '\n\n' + '#' * 100
            self.driver.get_screenshot_as_file('stop.png')
            handle_result()

    def get_result(self):

        print 'getting result....'

        fp = codecs.open('google_results.txt', 'a+', 'utf-8')
        a_elements = self.driver.find_elements_by_css_selector('h3>a')
        length = len(a_elements)

        for i in xrange(0, length):
            try:
                href = a_elements[i].get_attribute('href')
                site = re.search(u'/url\?q=(.*)&sa', href)
                if site:
                    site = site.groups()[0]
                    fp.write(site + '\n')

                    netloc = urlparse.urlparse(site).netloc
                    # print site_total, site
                    if netloc not in self.sites:
                        global site_total
                        site_total += 1
                        self.sites += netloc + ' '
                        print site_total, netloc

            except Exception, e:
                print e
                continue

        fp.close()


    def search(self):

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.useragent"] = (self.user_agent)
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.get(self.url)
        self.handle_captchar_limit(self.driver.current_url)
        self.get_result()

        # pages = total_result / 10
        pages = 100

        for i in xrange(1, pages+1):
            print '-' * 80
            print 'getting page ', i+1
            start = i * 10
            url = self.url + '&start=' + str(start)
            self.driver.get(url)
            self.handle_captchar_limit(self.driver.current_url)
            self.get_result()
            time.sleep(10)

        driver.quit()


def handle_result():

    print 'starting handling the result of google....'
    testresult = TestResult()
    testresult.test_visit('google_results.txt')
    print 'result has been handled, so quit...'
    sys.exit()


def main():

    try:
        google = Google()
        google.search()

    except KeyboardInterrupt:
        print 'press keyboardinterrupt, so quit....'
        google.driver.quit()


if __name__ == '__main__':
    os.system('clear')

    main()
