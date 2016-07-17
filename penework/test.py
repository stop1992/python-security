#encoding:utf-8

import os
import sys
import time


from lib.utils.crawler import crawler
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import paths


from setEnvironment import setEnv


def main():

    setEnv()

    # site = 'http://www.baidu.com'
    site = 'http://bbs.browser.qq.com'
    conf.crawlDepth = 10
    # print paths.USER_AGENTS
    crawler(site)


if __name__ == '__main__':
    os.system('clear')

    main()



