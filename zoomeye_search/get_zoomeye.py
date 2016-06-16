# encoding:utf-8

import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import sys
from urllib import unquote

try:
    import cPickle as pickle
except:
    import pickle

class ZoomEye(object):
    def __init__(self):

        self.file_name = 'discuz_7.2.txt'

        open(self.file_name, 'w').close()
        self.total_sites = 0

        # self.url_first = 'https://www.zoomeye.org/search?q=app%3Adiscuz%20php%3A%225.5.7%22'
        self.url_first = 'https://www.zoomeye.org/search?q=app%3A%22discuz%22+ver%3A%22X3.1%22'
        self.search_dork = unquote(self.url_first) + '&p=%s&t=web'


    def login(self):

        service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=https'
            ]

        self.driver = webdriver.PhantomJS(service_args=service_args)

        # fist step, get cookie by request url
        url = 'https://www.zoomeye.org/accounts/login/?next=/'
        self.driver.get(url)
        self.driver.refresh()
        self.driver.find_element(By.ID, 'id_username').send_keys('testone')
        self.driver.find_element(By.ID, 'id_password').send_keys('testone')

        self.driver.get_screenshot_as_file('login.png')
        captcha = raw_input('captcha:')
        self.driver.find_element(By.ID, 'id_captcha_1').send_keys(captcha)
        self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-info').click()
        # self.driver.set_window_size(height=1000, width=1000)
        # self.driver.get_screenshot_as_file('loged.png')

    def write_results2file(self):

        try:

            ul_element = self.driver.find_elements_by_css_selector('.result.web')[0]
            a_elements = ul_element.find_elements_by_css_selector('h3>a')

            # self.fp = open('zoomeye_results.txt', 'a+')
            self.fp = open(self.file_name, 'a+')

            for a in a_elements:
                self.total_sites += 1
                href = a.get_attribute('href')
                print self.total_sites, href
                self.fp.write(href + '\n')

            self.fp.close()

        except Exception, e:
            print e
            self.driver.get_screenshot_as_file('error.png')
            print 'get error page screenshot....'
            sys.exit()


    def get_result(self):

        self.login()

        if '/accounts/my/profile/' in self.driver.page_source:
            print 'login success'
        else:
            print 'not login, so login again....'
            self.login()

        print '-' * 80

        print 'getting page 1....'
        # search_dork = 'https://www.zoomeye.org/search?q=app%3Adiscuz%20php%3A%225.5.7%22&p=1&t=web'
        # search_dork = 'https://www.zoomeye.org/search?q=app%3A%22discuz%22%20ver%3A%227.2%22&p=1&t=web'

        self.driver.get(self.url_first)
        self.write_results2file()

        result_summary = self.driver.find_elements_by_class_name('result-summary')[0]
        result_counts = int(result_summary.text.split()[2])
        if result_counts%10:
            pages = result_counts / 10 + 1
        else:
            pages = result_counts / 10

        if pages > 50:
            pages = 50

        print 'total pages:', pages

        for page in xrange(2, pages+1):
            print '-' * 70
            print 'getting page ', page, '.....'
            self.driver.get(self.search_dork % str(page))
            print 'current search page:', self.driver.current_url
            self.write_results2file()
            time.sleep(60)

        driver.quit()


def main():

    zoom = ZoomEye()
    zoom.get_result()

if __name__ == '__main__':
    os.system('clear')

    main()
