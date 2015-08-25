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

        # key_words to store key words, last element to count post amounts
        key_words = [, 'post_amounts']
        # key words occur times amounts
        key_words_times = dict.fromkeys(key_words, 0)
        asktime = response.xpath(u'//*[@id="zwconttb"]/div[2]/text()').extract()
        if asktime:
            # from asktime get ask_time
            item['ask_time'] = asktime[0].split()[1]
            # from url get stock_num
            item['stock_num'] = response.url.split(',')[1]
            # compute key_words occur times in response.body
            for item in key_words:
                # print item
                pattern = re.compile(item)
                result = pattern.findall(response.body_as_unicode())
                if result:
                        # every item occur times in response.body
                        key_word_times = len(result)
                        # sum up every key word
                        key_words_times[item] += key_word_times
            key_words_times['key_word_times'] = 1 # represent post one time
            item['key_words'] = key_words_times
        # else:
                # item['asktime'] =  'null'
                # item['stock_num'] = 'null'
        yield item
