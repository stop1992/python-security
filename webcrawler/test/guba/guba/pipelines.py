# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class GubaPipeline(object):
	MONGODB_SERVER = '192.168.1.108'
	MONGODB_PORT = 27018
	MONGODB_DB = 'guba_data'

	def __init__(self):
		try:
			client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)
			self.db = client[self.MONGO_DB]
		except Exception, e:
			print str(e)
			traceback.print_exc()
		
		# self.file = codecs.open('guba.json', mode='w', encoding='utf-8')

	@classmethod
	def from_crawler(cls, crawler):
		cls.MONGODB_SERVER = crawler.settings.get('MONGO_SERVER', 'localhost')
		cls.MONGODB_PORT = crawler.settings.get('MONGO_PORT', 27018)
		cls.MONGODB_DB = crawler.settings.get('MONGO_DB', 'guba_data')
		pipe = cls()
		pipe.crawler = crawler
		return pipe
    
	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + '\n'
		self.file.write(line.decode('unicode-escape'))
		# self.file.close()
		print item
		return item
