# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field


class GubaItem(Item):
	ask_time = Field()
	stock_num = Field()
        replys_data = Field()
        # response = Field()
        # key_words = Field()
        # post_times = Field()
