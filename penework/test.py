#!/usr/bin/env python
# encoding: utf-8

import os
import pudb
import pdb


from lib.core.data import conf
from lib.core.enums import CUSTOM_LOGGING
from setEnvironment import setEnv
from setEnvironment import getConfig
# from lib.utils.crawler.getconfig import Config
from lib.utils.crawler.master import Master
# from lib.utils.crawler.master import Ma
from lib.utils.crawler.crawler import crawl
import pickle
from lib.core.data import logger


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
    testCrawler()


if __name__ == '__main__':
    os.system('clear')


    main()
