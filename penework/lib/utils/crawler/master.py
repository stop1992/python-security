#!/usr/bin/env python
# encoding: utf-8
# encoding: utf-8
# encoding: utf-8

from redis import Redis
from rq import Queue
import pudb
import re


from lib.core.data import conf
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.utils.crawler.crawlerDist import crawl
# from lib.utils.crawler.crawler import test
from lib.utils.urlOperate import hashUrl


class Master(object):

    def __init__(self):
        self.redisCon = Redis(host=conf.REDIS_HOST,
                              port=conf.REDIS_PORT,
                              password=conf.REDIS_PASSWD)
        self.jobQueue = Queue(connection=self.redisCon)
        map(lambda key: self.redisCon.delete(key), [key for key in self.redisCon.keys() if re.search('visit|rq:', key, re.I)])
        hashData = hashUrl(conf.CRAWL_SITE)
        self.redisCon.lpush('visit', conf.CRAWL_SITE)
        self.redisCon.sadd('visitSet', hashData)


    def start(self):

        countDepth = 0
        countUrls = 0

        while countDepth <= int(conf.CRAWL_DEPTH):

            while True:
                # wait for 10 minites
                # print 'len visite:', self.redisCon.llen('visit')
                # print 'len visited:', self.redisCon.scard('visited')
                url = self.redisCon.lpop('visit')
                if url:
                    countUrls += 1
                    print 'countDepth:', countDepth, 'countUrls:', countUrls
                    self.jobQueue.enqueue_call(crawl, args=(url, countDepth, countUrls))
                else:
                    self.redisCon.delete('visitSet')
                    break

            while True:
                # wait 30 seconds, if timeout, jobqueue is empty(except failed job)
                keyUrl = self.redisCon.blpop('tmpVisit', timeout=30)
                if keyUrl:
                    url = keyUrl[1]
                    hashData = hashUrl(url)
                    if not self.redisCon.sismember('visited', hashData) and \
                            not self.redisCon.sismember('visitSet', hashData):
                        self.redisCon.lpush('visit', url)
                        self.redisCon.sadd('visitSet', hashData)
                else:
                    break

            countDepth += 1
