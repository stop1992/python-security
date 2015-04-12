# -*- encoding:utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request

from doubanmovie.items import DoubanmovieItem

class DoubanmovieSpider(CrawlSpider):
	""" scrapy douban movie infomation """
	name = 'doubanmovie'
	allow_doumains = ['movie.douban.com']
	start_urls = [ 'http://movie.douban.com/top250' ]
	rules = [
		# request next page site
		Rule(LxmlLinkExtractor(allow='?start=\d+&filter=&type='),
			 callback='parse_next_site',
			 follow=True
			),
		# scrapy movie subject site
		Rule(LxmlLinkExtractor(allow=r'http://movie\.douban\.com/subject/\d+/'),
			 callback='parse_item',
			 follow=True
			)
	]

	def parse_next_site(self, response):
		print response.url


	def parse_item(self, response):
		sel = Selector(response)
		item = DoubanmovieItem()

		tmp_movie_name = sel.xpath('//div[@id="content"]/h1/span[1]/text()').extract()
		tmp_movie_director = sel.xpath('//div[@id="info"]/span[1]/span[2]/a/text()').extract()

		tmp_movie_starts = sel.xpath('').extract()

		tmp_movie_rating = sel.xpath('//div[@id="interest_sectl"]/div/p[1]/strong/text()').extract()

		item['movie_name']
