# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy import Field, Item


class DoubanmovieItem(Item):
	movie_name = Field()
	movie_director = Field()
	movie_writer = Field()
	movie_stars = Field()
	movie_rating = Field()
	movie_quote = Field
