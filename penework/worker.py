#!/usr/bin/env python
# encoding: utf-8

import os
from redis import Redis
from rq import Connection, Worker

from lib.core.data import conf
from setEnvironment import setEnv, getConfig


def main():

    setEnv()
    getConfig()

    redisCon = Redis(host=conf.REDIS_HOST,
                     port=conf.REDIS_PORT,
                     password=conf.REDIS_PASSWD)

    with Connection(connection=redisCon):
        qs = 'default'
        w = Worker(qs)
        w.work()
        print 'start worker successfully....'


if __name__ == '__main__':
    os.system('clear')

    main()
