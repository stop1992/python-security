# -*- encoding:utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
import traceback

from doubanmovie.items import DoubanmovieItem

class DoubanmovieSpider(CrawlSpider):
	""" scrapy douban movie infomation """
	name = 'doubanmovie'
	allow_doumains = ['movie.douban.com']
	start_urls = [ 'http://movie.douban.com/top250' ]
	download_delay = 2
	rules = [
	# request next page site
		Rule(LxmlLinkExtractor(allow=(r'\?start=\d+&filter=&type=',), 
							   deny=(r'http://movie\.douban\.com/subject/\d+/$',)),
		 callback='parse_next_site',
		 follow=True
		),
		Rule(LxmlLinkExtractor(allow=(r'http://movie\.douban\.com/subject/\d+/$',)),
		 callback='parse_item1',
		 follow=True
		)
	]

	def parse_next_site(self, response):

		#if response.status == 200:
			#Request
		print '\n\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print response.url
		raw_input('press any key to continue')
		print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'


	def parse_item1(self, response):
		if response.status == 403:
			yield Request(response.url, callback='parse_item1')

		sel = Selector(response)
		item = DoubanmovieItem()

		try:
			item['movie_name'] = sel.xpath('//div[@id="content"]/h1/span[1]/text()').extract()[0]
			soup = BeautifulSoup(response.body)
			spans = soup.find_all('span', class_='attrs')

			if len(spans) == 3:
				item['movie_director'] = spans[0].get_text()
				item['movie_writer'] = spans[1].get_text()
				item['movie_stars'] = spans[2].get_text()
			elif len(spans) == 2:
				item['movie_director'] = spans[0].get_text()
				item['movie_stars'] = spans[1].get_text()
				item['movie_writer'] = None

		except Exception:
			print '\n\n\n---------------------------------error------------------------'
			print traceback.print_exc()
			print response.url
			print '---------------------------------error------------------------'
			raw_input('press any key to continue')

		#return item
		yield item

	def parse_item2(self, response):
		if response.status == 403:
			print '\n\n---------------------------'
			print response.headers
			print response.request.headers
			print '-----------------------------'
			raw_input('press any key to continue')
		sel = Selector(response)
		item = DoubanmovieItem()

		try:
			item['movie_name'] = sel.xpath('//div[@id="content"]/h1/span[1]/text()').extract()[0]
			soup = BeautifulSoup(response.body)
			spans = soup.find_all('span', class_='attrs')
			if len(spans) == 3:
				item['movie_director'] = spans[0].get_text().replace(' ', '')
				item['movie_writer'] = spans[1].get_text().replace(' ', '') 
				item['movie_stars'] = spans[2].get_text().replace(' ', '') 
			elif len(spans) == 2:
				item['movie_director'] = spans[0].get_text().replace(' ', '')
				item['movie_writer'] = spans[1].get_text().replace(' ', '') 
		except Exception as ex:
			print '\n\n\n---------------------------------error------------------------'
			print traceback.print_exc()
			print ex.message
			print response.url
			print '---------------------------------error------------------------'
			raw_input('press any key to continue')
		
		yield item

		next_page_url = sel.xpath('//div[@id="content"]/div/div[1]/div[2]/span[3]/link/@href').extract()
		print '-----------------------------------------------'
		print len(next_page_url)
		for url in next_page_url:
			print url
		print '-----------------------------------------------'

		try:
			next_page_url = 'http://movie.douban.com/top250' + next_page_url
			yield Request(next_page_url, callback='parse_item2')
		except Exception as ex:
			print ex.message

