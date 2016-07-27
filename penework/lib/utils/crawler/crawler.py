#!/usr/bin/env python
#encoding:utf-8

from Queue import Queue
from bs4 import BeautifulSoup
import urlparse
import time
import re
from threading import Lock
import sys
import traceback

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

countVisitedUrls = 0


def _makeUrlHash(url):

    urlParse = urlparse.urlparse(url)
    urlSchemePath = urlparse.urljoin(urlParse.scheme, urlParse.netloc + urlParse.path)
    urlQueryKeys = (urlparse.parse_qs(urlParse.query)).keys()
    # combine urlSchemaPath and urlQueryKeys as urlHashData
    urlQueryKeys.append(urlSchemePath)
    urlQueryKeys.sort()
    hashData = hash(str(urlQueryKeys))

    return hashData


def crawler(target):

    visited = set()
    visitQueue = Queue()
    visitQueue.put(target)
    fp = open(paths.PENEWORK_ROOT_PATH + '/visited.txt', 'w')
    lock = Lock()
    headers = dict()

    currentDepth = 0

    def crawlerThread():
        global countVisitedUrls

        while visitQueue.qsize() > 0:
            url = visitQueue.get()

            headers[HTTP_HEADER.USER_AGENT] = randomUserAgents()
            try:
                if url not in visited:
                    response = requests.get(url, timeout=10, headers=headers)
                    crawlMsg = 'crawled %s depth: %d count: %d' % (url, currentDepth, countVisitedUrls)
                    logger.log(CUSTOM_LOGGING.SYSINFO, crawlMsg)
                    content = response.text

                    kb.pageEncoding = response.encoding
                    conf.cookie = str(response.cookies.get_dict())
                    hashData = _makeUrlHash(url)

                    lock.acquire()
                    visited.add(hashData)
                    fp.write(url + '\n')
                    countVisitedUrls += 1
                    lock.release()
                else:
                    continue
            except Exception, ex:
                logger.log(CUSTOM_LOGGING.ERROR, ex)
                print traceback.print_exc()
                continue

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
                            href = urlparse.urljoin(conf.domain, href)
                            if conf.domain in href:
                                links.put(href)

                except Exception, ex:  # for non-HTML files
                    logger.log(CUSTOM_LOGGING.ERROR, ex)
                    continue
                finally:
                    forms = findPageForms(content, url, False)
                    for form in forms:
                        formMsg = '%s has form, url: %s method: %s data: %s' % (url, form[0], form[1], form[2])
                        logger.log(CUSTOM_LOGGING.WARNING, formMsg)
                        lock.acquire()
                        fp.write(formMsg + '\n')
                        lock.release()


    while conf.crawlDepth >= currentDepth:

        links = Queue()
        # runThreads(conf.numThreads, crawlerThread)
        crawlerThread()

        while links.qsize() > 0:
            tmp_url = links.get()
            hashData = _makeUrlHash(tmp_url)
            if hashData not in visited:
               visitQueue.put(tmp_url)

        currentDepth += 1
    fp.close()
