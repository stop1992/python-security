#encoding:utf-8

import os
import sys
import time
import urlparse
import requests
import pdb

from lib.utils.crawler import crawler
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import paths
from lib.core.common import findPageForms
# from lib.core.data import formData

from setEnvironment import setEnv


def test():


    url = 'https://passport.csdn.net/account/login?ref=toolbar'
    response = requests.get(url)
    content = response.text
    kb.pageEncoding = response.encoding
    # conf.scope = 'https://passport.csdn.net'
    conf.scope = None
    conf.cookie = 'test=testa'
    # pdb.set_trace()
    forms = findPageForms(content, url, False, True)
    for form in forms:
        print form[0]
        print form[1]
        print form[2]


def main():

    setEnv()
    site = 'http://bbs.browser.qq.com/'
    conf.crawlDepth = 10
    conf.numThreads = 5
    conf.scope = None
    # conf.domain = 'bbs.browser.qq.com'
    conf.domain = site
    crawler(site)


if __name__ == '__main__':
    os.system('clear')

    main()
    # test()
