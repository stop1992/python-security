#-*- encoding:utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.http import Request
import re
from redis import Redis
# import cPickle as pickle

from guba.items import GubaItem

# server = Redis(host='192.168.1.108')

class GubaSpider(BaseSpider):
    name = 'guba'

    def start_requests(self):
        # while server.scard('stocks') > 0:
            # start = 'http://guba.eastmoney.com/list,' + server.spop('stocks') + ',f_1.html'
            # yield Request(url=start, callback=self.parse)
        directory = '.\stocknum_05'
        for stock_num in open(directory + '\stocknum_05_01.txt', 'r'):
            start = 'http://guba.eastmoney.com/list,' + stock_num.strip() + ',f_1.html'
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
            if detail_link and '/' in detail_link:
                # print '\033[2;31m yield detail link \033[1;m'
                yield Request(url=base_url+detail_link, callback=self.parse_detail)

    def parse_detail(self, response):
        item = GubaItem()

        asktime = response.xpath(u'//*[@id="zwconttb"]/div[2]/text()').extract()
        if asktime:
            tmp_ask_year = int(asktime[0].split()[1].split('-')[0])
            if tmp_ask_year >= 2013 and tmp_ask_year <= 2014:
                # from asktime get ask_time
                item['ask_time'] = asktime[0].split()[1]
                # from url get stock_num
                item['stock_num'] = 'db' + response.url.split(',')[1]
                replys_data = []
                xpath = ['//*[@id="zwconttbt"]', '//*[@id="zwconbody"]/div', '//div[@class="zwlitext stockcodec"]']
                for path in xpath:
                    data = response.xpath(path)
                    if data:
                        data = data.extract()
                        for text in data:
                            replys_data.append(text)
                if replys_data:
                    item['replys_data'] = replys_data
                else:
                    item['replys_data'] = None
            else:
                item = None
        else:
            item = None
        yield item
