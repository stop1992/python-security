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

from test_result import TestResult


class Google(object):

    def __init__(self):

        self.url = 'https://www.google.com/search?q=test'
        # self.url = 'https://www.google.com/search?q=inurl:login.php?id='
        self.user_agent = 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/47.0.2526.80 safari/537.36'
        codecs.open('google_results.txt', 'w', 'utf-8')

    def handle_captcha(self, url):

        first = True

        while 'sorry/indexredirect' in url:
            if first:
                print 'need captcha....'
            else:
                print 'captcha error, input captcha again'

            self.driver.get_screenshot_as_file('captcha.png')
            captcha = raw_input('captcha:')
            self.driver.find_element_by_id('captcha').send_keys(captcha)
            self.driver.find_element_by_name('submit').click()
            url = self.driver.current_url
        else:
            print 'do not need captcha'

    def get_result(self):

        fp = codecs.open('google_results.txt', 'a+', 'utf-8')
        a_elements = self.driver.find_elements_by_css_selector('h3>a')

        for a_element in a_elements:

            try:
                print '#' * 80
                href = a_element.get_attribute('href')
                # print 'href:', href
                site = re.search(u'/url\?q=(.*)&sa', href).groups()[0]
                print site
                fp.write(site + '\n')
            except Exception, e:
                print e
                continue

        fp.close()


    def search(self):

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.useragent"] = (self.user_agent)
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)

        # webdriver.desiredcapabilities.phantomjs['phantomjs.page.customheaders.useragent'] = self.user_agent
        # self.driver = webdriver.phantomjs()
        # self.driver = webdriver.firefox()

        self.driver.get(self.url)
        self.handle_captcha(self.driver.current_url)

        self.get_result()

        total_result = int(self.driver.find_element_by_id('resultStats').text.split()[1].replace(',',''))
        pages = total_result / 10

        for i in xrange(1, pages+1):

            print '-' * 80
            print 'getting page ', i+1
            start = i * 10
            url = self.url + '&start=' + str(start)
            self.driver.get(url)

            self.handle_captcha(self.driver.current_url)

            self.get_result()

            time.sleep(10)

        driver.quit()


def main():

    try:
        google = Google()
        google.search()

        testresult = TestResult()
        testresult.test_visit('google_results.txt')

    except KeyboardInterrupt:
        print 'press keyboardinterrupt, so quit....'
        google.driver.quit()
        testresult = TestResult()
        testresult.test_visit('google_results.txt')
        sys.exit()


if __name__ == '__main__':
    os.system('clear')

    main()
