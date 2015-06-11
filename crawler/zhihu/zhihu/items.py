# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# import scrapy
from scrapy import Item, Field 

class ZhihuItem(Item):
    # define the fields for your item here like:
	problem = Field()
	topics = Field()
	answers = Field()
	yesnum = Field()
	asktime = Field()
    # name = scrapy.Field()
    # pass
