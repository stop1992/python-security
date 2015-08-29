# -*- encoding:utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import traceback
#import types

from doubanmovie.items import DoubanmovieItem

class DoubanmovieSpider(Spider):

    name = 'moviespider'
    allow_domain = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']
    download_delay = 2

    def parse(self, response):

        print response.url
        pattern = re.compile(r'<a href="(http://movie.douban.com/subject/\d+/)" class="">')
        subjects = pattern.findall(response.body)

        num = 0
        for url in subjects:
            num += 1
            print num
            yield Request(url, callback=self.parse_subjects)

        pattern = re.compile(r'<a href="\?start=(\d+)&amp;filter=&amp;type=" >后页&gt;</a>')
        next_page = pattern.search(response.body)
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
                #raw_input('press any key to continue')

    def parse_subjects(self, response):
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
        yield item
