# -*- coding: utf-8 -*-

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting

from pymongo import MongoClient
import traceback


class GubaPipeline(object):

    def __init__(self):
        try:
            client = MongoClient(self.MONGODB_SERVER, int(self.MONGODB_PORT))
            self.db = client[self.MONGODB_DB]
        except Exception, e:
            print str(e)
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('MONGO_SERVER', 'localhost')
        cls.MONGODB_PORT = crawler.settings.get('MONGO_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('MONGO_DB', 'guba_data')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        if item:
            # use stock_num as collection
            post = self.db[item['stock_num']]
            # first get key words, then plus them ,then store
            post.insert({'ask_time':item['ask_time'],  'replys_data':item['replys_data']})


