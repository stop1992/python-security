# -*- encoding:utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from CSDNBlog.items import CsdnblogItem


class CSDNBlogCrawlSpider(CrawlSpider):
	"""inherit from CrawlSpider"""
	
	name = 'CSDNBlogCrawlSpider'
	download_delay = 1
	allow_domains = ['blog.csdn.net']
	start_urls = ['http://blog.csdn.net/u012150179/article/details/11749017']

	# method 1:
	"""
	rules = [
		Rule(LxmlLinkExtractor(
					allow=('/u012150179/article/details'),
					restrict_xpaths=('//li[@class="next_article"]'),
					follow=True)
	]"""
	# method 2:
	rules = [
		Rule(LxmlLinkExtractor(
					allow=('/u012150179/article/details'),
					restrict_xpaths=('//li[@class="next_article"]')),
					callback='para_item',
					follow=True)
	]

	def para_item(self, response):
		item = CsdnblogItem()
		sel = Selector(response)
		blog_url = str(response.url)
		blog_name = sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()

		item['blog_name'] = [ n.encode('utf-8') for n in blog_name ]
		item['blog_url'] = blog_url.encode('utf-8')

		yield item
