# -*-coding:utf-8-*-
#!/usr/bin/env python

import os
import threading
import urllib2
import re
import time

import chardet
import mythread


class OnePieceTieba:
    def __init__(self, url):
        self.url = url

    @profile
    def get_html_data(self):
        response = urllib2.urlopen(self.url)
        self.content = response.read()
        content_code = chardet.detect(self.content)
        if not content_code['encoding'] == 'utf-8':
            self.content.decode('utf-8')

    def extract_html_data(self):
        pattern = re.compile(
            ur'<a href="/p/\d+" title="[\u4e00-\u9fff\ufb00-\ufffd\s\S]+?" target="_blank" class="j_th_tit">[\u4e00-\u9fff\ufb00-\ufffd\s\S]+?</a>')
        result = pattern.findall(self.content)
        pattern = re.compile(
            ur'<a href="(/p/\d+)" title="[\u4e00-\u9fff\ufb00-\ufffd\s\S]+?" target="_blank" class="j_th_tit">([\u4e00-\u9fff\ufb00-\ufffd\s\S]+?)</a>')
        for i in range(len(result)):
            tmpre = pattern.search(result[i])
            print "tieba.baidu.com" + tmpre.group(1)
            print tmpre.group(2)

    def write2file(self):
        fp = open('onepiece.txt', 'w')
        fp.write(self.content)
        fp.close()


def get_urls():
    urls = []
    urls.append(u'http://tieba.baidu.com/f?ie=utf-8&kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&fr=search')
    #urls.append(u'http://tieba.baidu.com/f?kw=%E9%B8%A1%E6%AF%9B&fr=wwwt')
    #urls.append(u'http://tieba.baidu.com/f?kw=%E8%83%A1%E6%AD%8C&fr=wwwt')
    return urls


def handle_data(url):
    onepiece = OnePieceTieba(url)
    onepiece.get_html_data()
    onepiece.extract_html_data()


def main():
    urls = get_urls()
    urls_len = range(len(urls))

    # don't use mythread module to handle
    #for i in urls_len:
    #handle_data(urls[i])

    # using mythread module to handle
    threads = []
    for i in urls_len:
        tmp_thread = mythread.MyThread(func=handle_data, args=(urls[i],), name='test')
        threads.append(tmp_thread)
    for i in urls_len:
        threads[i].start()
    for i in urls_len:
        threads[i].join()


if __name__ == '__main__':
    os.system('printf "\033c"')

    #print 'starting time at:', time.ctime()
    main()
#print 'ending time at:', time.ctime()
