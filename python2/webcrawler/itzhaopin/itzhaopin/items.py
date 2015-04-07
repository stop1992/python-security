# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
#
#
#class ItzhaopinItem(scrapy.Item):
#    # define the fields for your item here like:
#    # name = scrapy.Field()
#    pass

from scrapy import Item, Field

class TencentItem(Item):
	name = Field()				
	catalog = Field()
	work_location= Field()
	recruit_number = Field()
	detail_link = Field()
	publish_time= Field()
