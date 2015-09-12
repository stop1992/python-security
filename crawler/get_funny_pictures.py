#!/usr/bin/env python
# encoding: utf-8

import os
import urllib
import re
import requests
from bs4 import BeautifulSoup
import lxml.html

def get_pictures():

    start_url = 'http://picture.ftng.net/all/1'
    response = requests.get(start_url)
    doc = lxml.html.fromstring(response.text)
    element = doc.xpath('//*[@id="pageNavigator"]/ul/li[7]/a')
    print element
    if element:
        pages = element[0]
        print pages
    else:
        print 'no data'

    # soup = BeautifulSoup(response.text)
    # soup.fin

if __name__ == '__main__':
    os.system('printf "\033c"')

    get_pictures()
