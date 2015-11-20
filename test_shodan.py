#!/usr/bin/env python
# encoding: utf-8

import os
import shodan
import requests

def test_shodan():

    pages = 100
    count = 0
    try:
        SHODAN_API_KEY = 'BgGlm7PGISqGOEieypFvUE0kuQtIBKeP'
        api = shodan.Shodan(SHODAN_API_KEY)
        results = api.search('apache', page=1)
        # print 'Result found: %s' % results['total']
        for result in results['matches']:
            request_cgi_bin(result['ip_str'])
            # print count, 'IP: ', result['ip_str']
            # count += 1
            # print 'data: ', result['data']
    except shodan.APIError, e:
        print 'Error: ', e

def request_cgi_bin(ip):
    url = 'http://' + ip + '/cgi-bin/'
    try:
        response = requests.get(url)
        print url, response.status_code
    except:
        pass


if __name__ == '__main__':
    os.system('clear')

    test_shodan()

