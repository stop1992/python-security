from scrapy.spider import Spider
from scrapy.http import FormRequest
from scrapy import log

class ZhihuSpider(Spider):
	
	name = 'zhihu'
	allow_domain = ['www.zhihu.com']
	# start_urls = 'http://www.zhihu.com/login'
	download_delay = 2

	def start_requests(self):
		return [FormRequest('http://www.zhihu.com/login', 
							formdata={'email':'1447932441@qq.com', 'password':'zhihuZHIHU68'},
							callback=self.after_login)]

	def after_login(self, response):
		log.start('log.txt')
		# print response.body
		log.msg(response.body)
		return 
