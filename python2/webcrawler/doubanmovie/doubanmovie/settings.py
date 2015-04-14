# -*- coding: utf-8 -*-

# Scrapy settings for doubanmovie project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'doubanmovie'

SPIDER_MODULES = ['doubanmovie.spiders']
NEWSPIDER_MODULE = 'doubanmovie.spiders'

COOKIES_ENABLED = False

ITEM_PIPELINES = {
	'doubanmovie.pipelines.DoubanmoviePipeline':300
}

DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':None,
	'doubanmovie.spiders.poll_useragent.PollUserAgentMiddleware':300
}

#LOG_LEVEL = 'ERROR'
#LOG_LEVEL = 'CRITICAL'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doubanmovie (+http://www.yourdomain.com)'
