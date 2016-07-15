# -*- encoding:utf-8 -*-

from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from CSDNBlog.items import CsdnblogItem

class CSDNBlogSpider(Spider):
    """
            scrapy csdn blog
    """

    name = 'CSDNBlog'
    download_delay = 1
    allowed_domains = ["blog.csdn.net"]
    start_urls = [
            # first article site
            "http://blog.csdn.net/u012150179/article/details/11749017"
    ]

    def parse(self, response):
        sel = Selector(response)

        item = CsdnblogItem()

        article_url = response.url
        article_name = sel.xpath('//div[@id="article_details"]/div[1]/h1/span/a/text()').extract()
        item['article_name'] = [ n.encode('utf-8') for n in article_name ]
        item['article_url'] = article_url.encode('utf-8')

        yield item

        # get next article site
        next_article_url = sel.xpath('//div[@id="article_details"]/ul/li/a/@href').extract()
        print len(next_article_url)
        raw_input('press any key to continue')
        for tmp_url in next_article_url:
                url = 'http://blog.csdn.net' + tmp_url
                print url
        yield Request(url, callback=self.parse)
