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

site_total = 0


class Google(object):

    def __init__(self):

        # self.url = 'https://www.google.com/search?q=test'
        # self.url = 'https://www.google.com/search?q=Powered+by+discuz&oq=Powered+by+discuz&aqs=chrome..69i57j69i60l3.7843j0j7&sourceid=chrome&es_sm=122&ie=UTF-8'
        # self.url = 'https://www.google.com.hk/search?newwindow=1&safe=strict&biw=1055&bih=538&q=intitle%3A%22%E7%B3%BB%E5%88%97%E4%BA%A7%E5%93%81%E5%8D%87%E7%BA%A7%22+inurl%3Aconvert&oq=intitle%3A%22%E7%B3%BB%E5%88%97%E4%BA%A7%E5%93%81%E5%8D%87%E7%BA%A7%22+inurl%3Aconvert&gs_l=serp.12...0.0.0.5808.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.owDUtoo3ZZY'
        self.url = 'https://www.google.com/search?q=inurl:faq.php%3Faction%3Dgrouppermission&newwindow=1&safe=active&biw=1055&bih=568&ei=BtiVVtWGA9i0jwOclJygDA&sa=N'
        # self.url = 'https://www.google.com/search?q=inurl:/viewthread.php?tid='
        # self.url = 'https://www.google.com/search?q=inurl:login.php?id='
        self.user_agent = 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/47.0.2526.80 safari/537.36'
        codecs.open('google_results.txt', 'w', 'utf-8')

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
            # raw_input('meet stop....')
            self.driver.get_screenshot_as_file('stop.png')
            handle_result()

    def get_result(self):

        print 'getting result....'

        fp = codecs.open('google_results.txt', 'a+', 'utf-8')

        a_elements = self.driver.find_elements_by_css_selector('h3>a')
        # self.driver.get_screenshot_as_file('page.png')

        length = len(a_elements)

        for i in xrange(0, length):

            try:
                href = a_elements[i].get_attribute('href')
                site = re.search(u'/url\?q=(.*)&sa', href)
                if site:
                    site = site.groups()[0]
                    fp.write(site + '\n')

                    global site_total
                    site_total += 1
                    print site_total, site

            except Exception, e:
                print e
                continue

        fp.close()


    def search(self):

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.useragent"] = (self.user_agent)
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)

        # webdriver.desiredcapabilities.phantomjs['phantomjs.page.customheaders.useragent'] = self.user_agent
        # self.driver = webdriver.Firefox()
        # self.driver = webdriver.Chrome('./chromedriver')

        self.driver.get(self.url)
        self.handle_captchar_limit(self.driver.current_url)
        self.get_result()

        # total_result = int(self.driver.find_element_by_id('resultStats').text.split()[1].replace(',',''))
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

            time.sleep(20)

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
        handle_result()

    except KeyboardInterrupt:
        print 'press keyboardinterrupt, so quit....'
        google.driver.quit()


if __name__ == '__main__':
    os.system('clear')

    main()
