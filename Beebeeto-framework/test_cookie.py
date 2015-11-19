#!/usr/bin/env python
# encoding: utf-8

import cookielib
import urllib
import urllib2
import os
import codecs
import requests

def test_cookie():
    cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)


    url = 'http://192.168.1.106/wordpress/wp-login.php'
    data = {
            'log':'admin',
            'pwd':'admin',
            'wp-submit':'Log+In',
            'redirect_to':'http%3A%2F%2F192.168.1.106%2Fwordpress%2Fwp-admin%2F',
            'testcookie':1
            }
    payload = urllib.urlencode(data)
    req = urllib2.Request(url, payload)
    content = urllib2.urlopen(req).read()
    print content
    fp = codecs.open('tmp.html', 'w', 'utf-8')
    fp.write(content)
    fp.close()

def test_req():
    url = 'http://192.168.1.106/wordpress/wp-login.php'
    get_response = requests.get(url)
    cookies = dict(get_response.cookies)
    print cookies

    data = {
            'log':'admin',
            'pwd':'admin',
            'wp-submit':'Log+In',
            'redirect_to':'http%3A%2F%2F192.168.1.106%2Fwordpress%2Fwp-admin%2F',
            'testcookie':1
            }
    post_response = requests.post(url, cookies=cookies, data=data)

    content = post_response.text
    print post_response.cookies
    fp = codecs.open('tmp.html', 'w', 'utf-8')
    fp.write(content)
    fp.close()

    # print response


if __name__ == '__main__':
    os.system('clear')

    test_req()

    # test_cookie()
