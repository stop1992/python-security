#!/usr/bin/env python
# encoding: utf-8
#encoding:utf-8

from Queue import Queue
from bs4 import BeautifulSoup
import urlparse
import time
import re
from threading import Lock
import sys
import traceback
from redis import Redis

from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import paths
from lib.core.enums import CUSTOM_LOGGING
from lib.core.enums import HTTP_HEADER
from lib.core.common import findPageForms
from lib.core.threads import runThreads
from lib.utils.userAgents import randomUserAgents
from thirdparty import requests
from lib.utils.urlOperate import hashUrl


# import copy_reg
# import types

# def _pickle_method(m):
    # if m.im_self is None:
        # return getattr, (m.im_class, m.im_func.func_name)
    # else:
        # return getattr, (m.im_self, m.im_func.func_name)

# copy_reg.pickle(types.MethodType, _pickle_method)


def crawl(url, currentDepth, countUrls):

    redisCon = Redis(host=conf.REDIS_HOST,
                      port=conf.REDIS_PORT,
                      password=conf.REDIS_PASSWD)
    # if redisCon.sismember('visited', url):
        # return

    try:
        headers = dict()
        headers[HTTP_HEADER.USER_AGENT] = randomUserAgents()

        response = requests.get(url, timeout=10, headers=headers)
        # crawlMsg = 'crawled %s depth: %d count: %d' % (url, currentDepth, countVisitedUrls)
        # logger.log(CUSTOM_LOGGING.SYSINFO, crawlMsg)
        content = response.text

        kb.pageEncoding = response.encoding
        conf.cookie = str(response.cookies.get_dict())
        hashData = hashUrl(url)
        redisCon.sadd('visited', hashData)
        redisCon.lpush('visitedList', url)

    except Exception, ex:
        logger.log(CUSTOM_LOGGING.ERROR, ex)
        print traceback.print_exc()
        return

    if isinstance(content, unicode):
        try:
            match = re.search(r"(?si)<html[^>]*>(.+)</html>", content)
            if match:
                content = "<html>%s</html>" % match.group(1)

            soup = BeautifulSoup(content, 'lxml')
            tags = soup('a')
            if not tags:
                tags = re.finditer(r'(?si)<a[^>]+href="(?P<href>[^>"]+)"', content)

            for tag in tags:
                href = tag.get("href") if hasattr(tag, "get") else tag.group("href")

                if href and 'javascript:' not in href:
                    href = urlparse.urljoin(conf.CRAWL_SITE, href)
                    if conf.CRAWL_SITE in href:
                        redisCon.lpush('tmpVisit', href)
                        # logger.log(CUSTOM_LOGGING.ERROR, href)

        except Exception, ex:  # for non-HTML files
            logger.log(CUSTOM_LOGGING.ERROR, ex)
        finally:
            forms = findPageForms(content, url, False)
            for form in forms:
                formMsg = '%s has form, url: %s method: %s data: %s' % (url, form[0], form[1], form[2])
                logger.log(CUSTOM_LOGGING.WARNING, formMsg)
