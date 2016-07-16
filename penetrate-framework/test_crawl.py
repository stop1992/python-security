import os
import sys

from lib.utils.crawler import crawl
from lib.core.data import conf
from lib.core.data import kb
from lib.core.option import initOptions
from lib.core.option import init
from lib.core.data import cmdLineOptions
from lib.parse.cmdline import cmdLineParser


def init():

    kb.threadContinue = True

    conf.showTime = True
    conf.crawlDepth = 10
    conf.sitemapUrl = ''
    conf.bulkFile = ''
    conf.threads = 1


def main():

    init()

    site = 'http://bbs.browser.qq.com'
    crawl(site)


if __name__ == '__main__':
    os.system('clear')

    main()
