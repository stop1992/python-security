#-*- encoding:utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.http import Request
import re
from redis import Redis

from guba.items import GubaItem

server = Redis(host='192.168.1.108')
class GubaSpider(BaseSpider):
	name = 'guba'
	# start_urls = ('http://guba.eastmoney.com/list,000002,f_1.html',)
	# start_urls = ('http://guba.eastmoney.com/list,' + server.spop('stock_num') + ',f_1.html',)
	
	def start_requests(self):
		while server.scard('stock_num') > 0:
			start = 'http://guba.eastmoney.com/list,' + server.spop('stock_num') + ',f_1.html'
			yield Request(url=start, callback=self.parse)

	def parse(self, response):
		pattern = re.compile(ur'共有帖子数 (\d+) 篇')
		tmp_search = pattern.search(response.body_as_unicode())
		total_posts = 0
		if tmp_search:
			total_posts = int(tmp_search.group(1))

		total_pages = total_posts / 80 + 1
		for i in xrange(2, total_pages + 1):
			next_link = ''
			base_url = response.url
			# get underline position
			underline_position = base_url.find('_')
			if underline_position > -1:
				next_link = base_url[0:underline_position+1] + str(i) + '.html'
			if next_link:
				# print '\033[2;31m yield url \033[1;m'
				yield Request(url=next_link, callback=self.parse)

		base_url = 'http://guba.eastmoney.com'
		for detail_link in response.xpath(u'//*[@id="articlelistnew"]/div/span[3]/a/@href').extract():
			if detail_link:
				# print '\033[2;31m yield detail link \033[1;m'
				yield Request(url=base_url+detail_link, callback=self.parse_detail)

	def parse_detail(self, response):
		item = GubaItem()

		key_words = []
		asktime = response.xpath(u'//*[@id="zwconttb"]/div[2]/text()').extract()
		if asktime:
			item['ask_time'] = asktime[0].split()[1]
			item['stock_num'] = response.url.split(',')[1]
			# compute key_words occur times in response.body
			for item in key_words:
				# print item
				pattern = re.compile(item)
				result = pattern.findall(response.body_as_unicode())
					if result:
						for i in result:
							print i, 'in b'

		else:
			item['asktime'] =  'null'
			item['stock_num'] = 'null'
		yield item
