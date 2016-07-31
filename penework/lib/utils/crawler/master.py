#!/usr/bin/env python
# encoding: utf-8

from redis import Redis
from rq import Queue


from lib.core.data import conf
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.utils.crawler.crawler import crawl
# from lib.utils.crawler.crawler import test
from lib.utils.hashUrl import hashUrl


class Master(object):

    def __init__(self):
        self.redisCon = Redis(host=conf.REDIS_HOST,
                          port=conf.REDIS_PORT,
                          password=conf.REDIS_PASSWD)
        self.jobQueue = Queue(connection=self.redisCon)

        self.redisCon.delete('visited')
        self.redisCon.delete('visit')

        # while self.redisCon.scard('visited') > 0:
            # self.redisCon.srem('visited')
        # while self.redisCon.llen('visit') > 0:
            # self.redisCon.lpop('visit')

        # if self.redisCon.llen('visit') == 0 and self.redisCon.scard('visited') == 0:
        self.redisCon.lpush('visit', conf.CRAWL_SITE)

    def start(self):

        currentDepth = 0

        while currentDepth <= conf.CRAWL_DEPTH:

            # while self.redisCon.llen('visit') > 0:
            while True:
                # wait for 10 minites
                # print 'len visite:', self.redisCon.llen('visit')
                # print 'len visited:', self.redisCon.scard('visited')
                listData = self.redisCon.blpop('visit', timeout=5)
                if listData:
                    url = listData[1]
                    hashData = hashUrl(url)
                    if not self.redisCon.sismember('visited', hashData):
                        self.jobQueue.enqueue_call(crawl, args=(url, currentDepth))
                        logger.log(CUSTOM_LOGGING.SYSINFO, 'entering ' + url)
                else:
                    break


            while self.redisCon.llen('tmp_visit') >0:
                listData = self.redisCon.lpop('tmp_visit')
                if listData:
                    url = listData[1]
                    self.redisCon.lpush('visit', url)

            currentDepth += 1




