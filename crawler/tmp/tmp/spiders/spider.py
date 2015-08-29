#!/usr/bin/env python
# encoding: utf-8

from scrapy.spider import BaseSpider
from scrapy.http import Request

from tmp.items import TmpItem

class TestSpider(BaseSpider):
    name = 'tt'

    def start_requests(self):
        url = 'http://www.baidu.com'
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = TmpItem()
        tmp = ['daitao', 'wangxi', 'test']
        item['test'] = tmp
        yield item
