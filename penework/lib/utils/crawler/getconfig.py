#encoding:utf-8

from ConfigParser import ConfigParser
import os


from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.data import paths


class Config(object):

    def __init__(self):

        try:

            self.config = ConfigParser()
            print os.path.realpath('.')
            configFile = paths.PENEWORK_ROOT_PATH + '/penework.conf'
            self.config.read(configFile)
            self.section = 'Crawler'
            self.REDIS_HOST = self.config.get(self.section, 'REDIS_HOST')
            self.REDIS_PORT = self.config.get(self.section, 'REDIS_PORT')
            self.REDIS_PASSWD = self.config.get(self.section, 'REDIS_PASSWD')
            self.CRAWL_SITE = self.config.get(self.section, 'crawl_siter')

        except Exception, ex:
            logger.log(CUSTOM_LOGGING.ERROR, 'get config error: ' + ex.message)


# if __name__ == '__main__':
    # config = Config()
    # print config.REDIS_HOST
