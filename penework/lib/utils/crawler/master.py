#!/usr/bin/env python
# encoding: utf-8
# encoding: utf-8

from redis import Redis
from rq import Queue
import pudb


from lib.core.data import conf
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.utils.crawler.crawlerDist import crawl
# from lib.utils.crawler.crawler import test
from lib.utils.hashUrl import hashUrl


class Master(object):

    def __init__(self):
        self.redisCon = Redis(host=conf.REDIS_HOST,
                          port=conf.REDIS_PORT,
                          password=conf.REDIS_PASSWD)
        self.jobQueue = Queue(connection=self.redisCon)
        map(lambda key: self.redisCon.delete(key), [key for key in self.redisCon.keys() if 'visit' in key or 'rq:' in key])
        self.redisCon.lpush('visit', conf.CRAWL_SITE)


    def start(self):

        currentDepth = 0
        countUrls = 0

        while currentDepth <= conf.CRAWL_DEPTH:

            while True:
                # wait for 10 minites
                # print 'len visite:', self.redisCon.llen('visit')
                # print 'len visited:', self.redisCon.scard('visited')
                url = self.redisCon.lpop('visit')
                # if listData:
                    # url = listData[1]
                if url:
                    countUrls += 1
                    # if countUrls > 5000:
                    pudb.set_trace()
                    print 'currentDepth:', currentDepth
                    self.jobQueue.enqueue_call(crawl, args=(url, currentDepth, countUrls))
                else:
                    # failedQueue = self.redisCon.llen('rq:failed'
                    break

            while self.redisCon.llen('tmpVisit') >0:
                # wait 30 seconds, if timeout, jobqueue is empty(except failed job)
                keyUrl = self.redisCon.blpop('tmpVisit', timeout=30)
                if keyUrl:
                    url = keyUrl[1]
                    hashData = hashUrl(url)
                    if not self.redisCon.sismember('visited', hashData):
                        self.redisCon.lpush('visit', url)

            currentDepth += 1


