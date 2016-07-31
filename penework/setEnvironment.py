#!/usr/bin/env python
# encoding: utf-8
# encoding: utf-8

import os
from ConfigParser import ConfigParser

from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.common import setPaths
from lib.core.data import paths
from lib.core.data import conf



def setEnv():

    paths.PENEWORK_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    setPaths()


def getConfig():

    try:

        config = ConfigParser()
        configFile = paths.PENEWORK_ROOT_PATH + '/penework.conf'
        config.read(configFile)
        crawl_section = 'Crawler'
        conf.REDIS_HOST = config.get(crawl_section, 'REDIS_HOST')
        conf.REDIS_PORT = config.get(crawl_section, 'REDIS_PORT')
        conf.REDIS_PASSWD = config.get(crawl_section, 'REDIS_PASSWD')
        conf.CRAWL_SITE = config.get(crawl_section, 'CRAWL_SITE')
        conf.CRAWL_DEPTH = config.get(crawl_section, 'CRAWL_DEPTH')

    except Exception, ex:
        logger.log(CUSTOM_LOGGING.ERROR, 'get config error: ' + ex.message)


