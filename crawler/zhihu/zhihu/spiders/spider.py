from scrapy_redis.spiders import RedisMixin

from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from scrapy.spider import Spider
from bs4 import BeautifulSoup
# from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
import traceback
import re
from scrapy import log

from zhihu.items import ZhihuItem

# class ZhihuSpider(RedisMixin, CrawlSpider):
class ZhihuSpider(Spider, RedisMixin):
	""" 
		ZhihuSpider inherit RedisMixin(by this to use redis),
		inherit CrawlSpider to use Rule
	"""
	def set_crawler(self, crawler):
		super(ZhihuSpider, self).set_crawler(crawler)
		self.setup_redis()

	name = 'zhihu'
	all_domain = ['www.zhihu.com']
	# start_urls = ['http://www.zhihu.com/topic/19776749/questions?page=1']
	# start_urls = ['http://www.zhihu.com/login']
	# start_urls = ['http://www.zhihu.com/#signin']

	download_delay = 2
	#rules = [
	#	Rule(LxmlLinkExtractor(allow=(r'\?page=\d+'),
	#						   deny=(r'/question/\d+')),
	#		callback='parse_next_page',
	#		follow=True
	#	),
	#	Rule(LxmlLinkExtractor(allow=(r'/question/\d+')),
	#		 callback='parse_item',
	#		 follow=True
	#		 )
	#]

	# def parse(self, response):
		# print response.body
		# return 
	# def parse(self, response):
		# return FormRequest.from_response(
					# response, 
					# formdata={'email':'1447932441@qq.com', 'password':'zhihuZHIHU68'},
					# callback=self.after_login)

	def start_requests(self):
		return [FormRequest(
					'http://www.zhihu.com/login',
					formdata={'email':'1447932441@qq.com', 'password':'zhihuZHIHU68'},
					callback=self.after_login)]

	def parse_next_page(self, response):
		# url = 'http://www.zhihu.com' + 
		soup = BeautifulSoup(response.body)
		# pattern_time = re.compile(r'<span class="time" data-timestamp="\d+">

		# yield Request(
		# pass

	def after_login(self, response):
		# log.start('log.txt')
		print response.body
		return 
		# log.msg(response.body)
		# url = 'http://www.zhihu.com/topic/19776749/questions?page=1'
		# yield Request(url, callback=self.parse_item)

	def parse_item(self, response):
		items = ZhihuItem()
		soup = BeautifulSoup(response.body)
		anums = soup.find_all('a')
		for item in anums:
			items['yesnum'] = item

		yield items

		# print response.url
		# return 
		# print response.
		# pass
