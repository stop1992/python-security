#!/usr/bin/env python
# encoding: utf-8

from scrapy.spider import BaseSpider
from scrapy.http import Request

from test.items import TestItem

class TestSpider(BaseSpider):
    name = 'tt'

    def start_requests(self):
        url = 'http://www.baidu.com'
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = TestItem()
        tmp = ['daitao', 'wangxi']
        item['test'] = tmp
        yield item
