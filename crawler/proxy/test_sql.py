#!/usr/bin/env python
# encoding: utf-8

import os
import re
import requests

def test_sql():
    proxies = {
            'http':'123.56.110.227:8080',
            'https':'123.56.110.227:8080'
            }
    url = 'http://www.youku.com'
    url = 'http://www.tudou.com'
    response = requests.get(url, proxies=proxies)
    print response
    response = requests.get(url)
    print response

def main():
    test_sql()

if __name__ == '__main__':
    os.system('clear')

    main()
