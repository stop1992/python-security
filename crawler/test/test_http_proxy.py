#encoding:utf-8

import os
import urllib2
import requests
from selenium import webdriver

def test_proxy():
    # proxy_support = urllib2.ProxyHandler({'http':'http://113.139.154.33:8090'})
    # proxy_support = urllib2.ProxyHandler({'http':'http://112.103.46.74:8090'})
    # proxy_support = urllib2.ProxyHandler({'http':'http://125.224.112.235:8088'})
    proxy_support = urllib2.ProxyHandler({'http':'http://124.251.62.246:80'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    for i in xrange(50):
        try:
            url = 'http://www.zhihu.com'
            response = urllib2.urlopen(url)
            # print response.read()
            print response.getcode()
        except Exception, e:
            print e
            continue

def webdriver_proxy():
    url = 'http://www.zhihu.com'
    url = 'https://www.taobao.com'
    service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=https'
            ]
    # driver = webdriver.PhantomJS(desired_capabilities={'proxy':'http://124.251.62.246:80'})
    driver = webdriver.PhantomJS(service_args=service_args)
    # driver = webdriver.PhantomJS()
    # for i in xrange(50):
    driver.get(url)
    print driver.title
    print driver.page_source
    driver.quit()


if __name__ == '__main__':
    os.system('clear')

    webdriver_proxy()
    # test_proxy()
