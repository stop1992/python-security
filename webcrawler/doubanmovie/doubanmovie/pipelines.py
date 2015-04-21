# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class DoubanmoviePipeline(object):
	def __init__(self):
		self.file = codecs.open('doubanmovie_data.json', mode='w', encoding='utf-8')
	
	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + '\n'
		self.file.write(line.decode('unicode-escape'))
		#print item
		return item
		#return None
