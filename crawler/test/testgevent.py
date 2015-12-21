#!/usr/bin/env python
# encoding: utf-8

from gevent import monkey; monkey.patch_all()
import gevent
import urllib2
import os

def f(url):
    for i in xrange(1000):
        print 'get: ', url
        response = urllib2.urlopen(url)
        data = response.read()
        print 'received data len:', len(data)

if __name__ == '__main__':
    os.system('printf "\033c"')

    gevent.joinall([
        gevent.spawn(f, 'http://www.baidu.com'),
        gevent.spawn(f, 'http://www.taobao.com'),
        gevent.spawn(f, 'http://www.zhihu.com'),
        gevent.spawn(f, 'http://www.youku.com'),
        gevent.spawn(f, 'http://www.tudou.com'),
        gevent.spawn(f, 'http://www.qq.com')
        ])
