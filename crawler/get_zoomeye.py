# encoding:utf-8

# import requests
import os
# import re
# from bs4 import BeautifulSoup
# import urllib
# import urllib2
# import cookielib
from selenium import webdriver
import time
# import pdb
from selenium.webdriver.common.by import By
import sys

try:
    import cPickle as pickle
except:
    import pickle

class ZoomEye(object):
    def __init__(self):
        pass

    def login(self):

        service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=https'
            ]

        self.driver = webdriver.PhantomJS(service_args=service_args)

        # fist step, get cookie by request url
        # url = 'https://www.zoomeye.org'
        url = 'https://www.zoomeye.org/accounts/login/?next=/'
        self.driver.get(url)
        self.driver.refresh()
        self.driver.find_element(By.ID, 'id_username').send_keys('testone')
        self.driver.find_element(By.ID, 'id_password').send_keys('testone')
        # self.driver.get_screenshot_as_file('frist.png')
        self.driver.get_screenshot_as_file('login.png')
        # raw_input('get first screenshot....')
        captcha = raw_input('captcha:')
        self.driver.find_element(By.ID, 'id_captcha_1').send_keys(captcha)
        self.driver.find_element(By.CSS_SELECTOR, '.btn.btn-info').click()
        self.driver.set_window_size(height=1000, width=1000)
        self.driver.get_screenshot_as_file('loged.png')

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

        self.login()

        # if u'退出登录' in self.driver.page_source:
        if '/accounts/my/profile/' in self.driver.page_source:
            print 'login success'
        else:
            print 'not login, so login again....'
            self.login()
            # self.driver.quit()
            # sys.exit()

        # raw_input('so wait .....')

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
            time.sleep(30)

        driver.quit()


def main():
    zoom = ZoomEye()
    zoom.get_result()

if __name__ == '__main__':
    os.system('clear')

    main()
