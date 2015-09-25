#!/usr/bin/env python
# encoding: utf-8

import os
import urllib
import re
import requests
from bs4 import BeautifulSoup
import lxml.html
import gevent
# import ipdb

IMAGE_NUMS = 1

def get_all_pages():

    start_url = 'http://picture.ftng.net/all'
    response = requests.get(start_url)
    doc = lxml.html.fromstring(response.text)
    element = doc.xpath('//*[@id="pageNavigator"]/ul/li[7]/a')
    # print element
    if element:
        pages = element[0]
        return pages.text
    else:
        return 0

def get_all_pictures(page):
    start_url = 'http://picture.ftng.net/all/' + str(page)
    print 'handling ', start_url
    # headers = {'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"}

    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Referer:http":"//picture.ftng.net/all/2",
               "Upgrade-Insecure-Requests":1,
               "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36" }

    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language":"zh-CN,en-US;q=0.7,en;q=0.3",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie":"CNZZDATA2372878=cnzz_eid%3D827158635-1442065066-%26ntime%3D1442118663; JSESSIONID=3DC58F735D3E9BC4FF9BC983445301D1; all=2",
            # "Cookie":"JSESSIONID=6C5E5FBB6501695BC2F1D98C3DD7A0C1; all=2; CNZZDATA2372878=cnzz_eid%3D827158635-1442065066- %26ntime%3D1442065066",
            "Host":"picture.ftng.net",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0" }

    response = requests.get(start_url, headers=headers)
    # print 'request done....'
    if len(response.text) > 5000:
        # print 'pages request successfully....'
        soup = BeautifulSoup(response.text)
        result = soup.find_all('img', class_="img-thumbnail")
        # ipdb.set_trace()
        # image_nums = 1
        for line in result:
            print '-----------------------------------'
            img_url = line['src']
            include_http = re.search('http', img_url)
            if include_http:
                # print img_url
                image_attri = img_url[(img_url.index('?')-3):img_url.index('?')]
                global IMAGE_NUMS
                image_name = str(IMAGE_NUMS) + '.' + image_attri
                IMAGE_NUMS += 1
                image = requests.get(img_url)
                fp = open(image_name, 'w')
                fp.write(image.content)
                fp.close()
                print image_name
                os.system('mv ' + image_name + ' ./images/')
                # raw_input('please enter...')
    else:
        print 'pages request error....'

def gevent_execute(i):
    gevent.joinall([
            gevent.spawn(get_all_pictures, i),
            gevent.spawn(get_all_pictures, i+1),
            gevent.spawn(get_all_pictures, i+2),
            gevent.spawn(get_all_pictures, i+3),
            gevent.spawn(get_all_pictures, i+4),
            gevent.spawn(get_all_pictures, i+5),
            gevent.spawn(get_all_pictures, i+6),
            ])

if __name__ == '__main__':
    os.system('printf "\033c"')
    os.system('rm -rf images')
    os.system('mkdir images')

    pages = int(get_all_pages())
    print 'total pages:', pages

    i = 2
    while i < pages:
        get_all_pictures(i)
        i = i+1
        # i += 7
