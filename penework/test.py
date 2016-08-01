#!/usr/bin/env python
# encoding: utf-8

import os
import pudb
import pdb
import pickle
import sys
import codecs


from lib.core.data import conf
from lib.core.enums import CUSTOM_LOGGING
from setEnvironment import setEnv
from setEnvironment import getConfig
from lib.utils.crawler.master import Master
from lib.utils.crawler.crawler import crawl
from lib.core.data import logger
from lib.utils.hashUrl import hashUrl


def testHashurl():
    fp = codecs.open(conf.STORE_FILENAME, 'r', 'utf-8')
    wfp = codecs.open('check.txt', 'w', 'utf-8')
    for url in fp:
        url = url.strip()
        msg = url + ' ' + hashUrl(url)
        wfp.write(msg + '\n')
    wfp.close()
    print 'write successfully....'


def testCrawler():

    crawl(conf.CRAWL_SITE)


def testCrawlerDist():
    master = Master()
    # pudb.set_trace()
    logger.log(CUSTOM_LOGGING.SYSINFO, 'starting rq server...')
    master.start()
    logger.log(CUSTOM_LOGGING.SYSINFO, 'start rq server successfully...')


def main():

    setEnv()
    getConfig()
    # testHashurl()
    # testCrawler()


if __name__ == '__main__':
    os.system('clear')


    main()
