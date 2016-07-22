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


def main():

    setEnv()
    # site = 'http://bbs.browser.qq.com/'
    # site = 'http://www.jlu.edu.cn/'
    site = 'http://www.dhu.edu.cn/'
    conf.crawlDepth = 10
    conf.numThreads = 5
    conf.scope = None
    # conf.domain = 'bbs.browser.qq.com'
    conf.domain = site
    # pdb.set_trace()
    crawler(site)


if __name__ == '__main__':
    os.system('clear')

    main()
    # test()
