# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field


class GubaItem(Item):
	ask_time = Field()
	stock_num = Field()
        key_words = Field()
        post_times = Field()
