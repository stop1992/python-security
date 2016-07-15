# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy import Item, Field


class CsdnblogItem(Item):
    blog_name = Field()
    blog_url = Field()
    #article_name = Field()
    #article_url = Field()
