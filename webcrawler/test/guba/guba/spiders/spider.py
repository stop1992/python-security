#-*- encoding:utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.http import Request
import re

from guba.items import GubaItem

class GubaSpider(BaseSpider):
	name = 'guba'
	start_urls = ('http://guba.eastmoney.com/list,000002,f_1.html',)

	def parse(self, response):
		# response_selector = HtmlXPathSelector(response)
		# next_link = response_selector.select(u'//*[@id="articlelistnew"]/div[92]/span/span/a[13]').extract()[0]
		# next_link = response.xpath(u'//*[@id="articlelistnew"]/div[92]/span/span/a[13]').extract()[0]
		# pattern = re.compile(ur'共有t
		pattern = re.compile(ur'共有帖子数 (\d+) 篇')
		tmp_search = pattern.search(response.body_as_unicode())
		total_posts = 0
		if tmp_search:
			total_posts = int(tmp_search.group(1))

		print total_posts

		total_pages = total_posts / 80 + 1
		print total_pages
		# total_pages = 1000
		# raw_input('please enter any key\n\n\n')
		for i in xrange(2, total_pages + 1):
			next_link = ''
			base_url = response.url
			# get underline position
			underline_position = base_url.find('_')
			if underline_position > -1:
				next_link = base_url[0:underline_position+1] + str(i) + '.html'
			if next_link:
				print '\033[2;31m yield url \033[1;m'
				yield Request(url=next_link, callback=self.parse)

		base_url = 'http://guba.eastmoney.com'
		for detail_link in response.xpath(u'//*[@id="articlelistnew"]/div/span[3]/a/@href').extract():
			if detail_link:
				print '\033[2;31m yield detail link \033[1;m'
				yield Request(url=base_url+detail_link, callback=self.parse_detail)

	def parse_detail(self, response):
		item = GubaItem()

		asktime = response.xpath(u'//*[@id="zwconttb"]/div[2]/text()').extract()
		if asktime:
			item['asktime'] = asktime[0]
		else:
			item['asktime'] =  'null'
		yield item
