# -*- encoding:utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup

from doubanmovie.items import DoubanmovieItem

class DoubanmovieSpider(CrawlSpider):
	""" scrapy douban movie infomation """
	name = 'doubanmovie'
	allow_doumains = ['movie.douban.com']
	start_urls = [ 'http://movie.douban.com/top250' ]
	download_delay = 2
	#rules = [
		# request next page site
	"""
	Rule(LxmlLinkExtractor(allow='?start=\d+&filter=&type='),
		 callback='parse_next_site',
		 follow=True
		),
	"""
		# scrapy movie subject site
	rules = [
		Rule(LxmlLinkExtractor(allow=(r'http://movie\.douban\.com/subject/\d+/')),
			 callback='parse_item',
			 follow=True
			)
	]

	#def parse_next_site(self, response):
		#print response.url


	def parse_item(self, response):
		sel = Selector(response)
		item = DoubanmovieItem()

		tmp_movie_name = sel.xpath('//div[@id="content"]/h1/span[1]/text()').extract()[0]
		item['movie_name'] = tmp_movie_name.encode('utf-8')
		soup = BeautifulSoup(response.body)
		spans = soup.find_all('span', class_='attrs')
		item['movie_director'] = spans[0].get_text().encode('utf-8').replace(' ', '')
		item['movie_writer'] = spans[1].get_text().encode('utf-8').replace(' ', '')
		item['movie_stars'] = spans[2].get_text().encode('utf-8').replace(' ', '')

		return item

	def parse_item2(self, response):
		sel = Selector(response)
		item = DoubanmovieItem()

		try:
			tmp_movie_name = sel.xpath('//div[@id="content"]/h1/span[1]/text()').extract()[0]
		except Exception as ex:
			print ex
			raw_input('press any key to continue')
			

		item['movie_name'] = tmp_movie_name.encode('utf-8')
		soup = BeautifulSoup(response.body)
		spans = soup.find_all('span', class_='attrs')
		item['movie_director'] = spans[0].get_text().encode('utf-8').replace(' ', '')
		item['movie_writer'] = spans[1].get_text().encode('utf-8').replace(' ', '')
		item['movie_stars'] = spans[2].get_text().encode('utf-8').replace(' ', '')

		yield item

		next_page_url = sel.xpath('//div[@id="content"]/div/div[1]/div[2]/span[3]/link/@href').extrat()
		next_page_url = 'http://movie.douban.com/top250' + next_page_url
		yield Request(next_page_url, callback='parse_item2')

