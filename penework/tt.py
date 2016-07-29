#encoding:utf-8

import os
import urlparse

from setEnvironment import setEnv
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from Queue import Queue


countVisitedUrls = 0

def main():


    # logger.log(CUSTOM_LOGGING.SYSINFO, 'this is a test')
    # print os.path.dirname(os.path.realpath(__file__))
    # a = 0
    # countVisitedUrls = 0
    url = 'http://www.qq.com'
    t = 'http://www.baidu.com/test.php'
    u = urlparse.urljoin(url, t)
    print u

    def test():
        global countVisitedUrls
        # global countVisitedUrls
        # print countVisitedUrls
        print countVisitedUrls
        countVisitedUrls += 1


if __name__ == '__main__':
    os.system('clear')

    main()


