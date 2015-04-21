# -*- encoding:utf-8 -*-

from scrapy.spider import Spider
#from srapy.selector import Selector
from scrapy.http import Request
#from bs4 import BeautifulSoup
import re
import traceback
import types

#from doubanmovie.items import DoubanmovieItem

class DoubanmovieSpider(Spider):

	name = 'moviespider'
	allow_domain = ['movie.douban.com']
	start_urls = ['http://movie.douban.com/top250']
	download_delay = 3

	def parse(self, response):

		print response.url
		pattern = re.compile(r'<a href="(http://movie.douban.com/subject/\d+/)" class="">')
		subjects = pattern.findall(response.body)

		for url in subjects:
			yield Request(url, callback=self.parse_subjects)

		pattern = re.compile(r'<a href="\?start=(\d+)&amp;filter=&amp;type=" >后页&gt;</a>')
		next_page = pattern.search(response.body)
		#if next_page == types.NoneType:
			#return None
			#yield None
		#print len(next_page)
		try:
			if next_page.group(1):
				next_page_url = 'http://movie.douban.com/top250?start='\
					+str(next_page.group(1))+'&filter=&type='
				yield Request(url=next_page_url, callback=self.parse)
		except Exception:
			print '\n\n\n##########################################################'
			traceback.print_exc()
			print response.url
			print '###############################################################\n\n'
			raw_input('press any key to continue')

	def parse_subjects(self, response):
		print '\n\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print response.url
		print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		#raw_input('press any key to continue')
		return None
		#yield 'test'

