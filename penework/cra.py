# encoding:utf-8

import os
import pudb
import pdb


from setEnvironment import setEnv
from lib.utils.crawler.getconfig import Config



def main():

    setEnv()
    pudb.set_trace()
    config = Config()
    print config.REDIS_HOST


if __name__ == '__main__':
    os.system('clear')

    main()
