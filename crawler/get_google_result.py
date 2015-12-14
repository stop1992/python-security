# encoding:utf-8

import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

class Google(object):

    def __init__(self):

        self.url = 'https://www.google.com/search?q=test'

    def search(self):

        service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=http'
            ]

        self.driver = webdriver.PhantomJS(service_args=service_args)


        driver

