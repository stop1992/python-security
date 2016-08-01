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
import pudb
import pdb
import codecs

from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import paths
from lib.core.enums import CUSTOM_LOGGING
from lib.core.enums import HTTP_HEADER
from lib.core.common import findPageForms
from lib.core.threads import runThreads
from lib.utils.hashUrl import hashUrl
from lib.utils.userAgents import randomUserAgents
from thirdparty import requests

countVisitedUrls = 0


def crawl(target):

    visited = set()
    visitQueue = Queue()
    visitQueue.put(target)
    hashData = hashUrl(target)
    visitSet.add(hashData)
    fp = codecs.open(paths.PENEWORK_ROOT_PATH+'/'+conf.STORE_FILENAME, 'w', 'utf-8')
    lock = Lock()
    headers = dict()

    currentDepth = 0

    def crawlerThread():
        global countVisitedUrls

        while visitQueue.qsize() > 0:
            url = visitQueue.get()
            try:
                hashData = hashUrl(url)
                if hashData not in visited:
                    headers[HTTP_HEADER.USER_AGENT] = randomUserAgents()
                    response = requests.get(url, timeout=10, headers=headers)
                    crawlMsg = 'crawled %s depth: %d count: %d' % (url, currentDepth, countVisitedUrls)
                    logger.log(CUSTOM_LOGGING.SYSINFO, crawlMsg)
                    content = response.text

                    kb.pageEncoding = response.encoding
                    conf.cookie = str(response.cookies.get_dict())

                    try:
                        lock.acquire()
                        visited.add(hashData)
                        countVisitedUrls += 1
                        fp.write(url + '\n')
                        lock.release()
                    except Exception, ex:
                        logger.log(CUSTOM_LOGGING.ERROR, ex)
                        if lock.locked():
                            lock.release()
                        continue
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
                            href = urlparse.urljoin(conf.CRAWL_SITE, href)
                            if conf.CRAWL_SITE in href:
                                links.put(href)

                except Exception, ex:  # for non-HTML files
                    logger.log(CUSTOM_LOGGING.ERROR, ex)
                    continue
                finally:
                    forms = findPageForms(content, url, False)
                    for form in forms:
                        formMsg = '%s has form, url: %s method: %s data: %s' % (url, form[0], form[1], form[2])
                        logger.log(CUSTOM_LOGGING.WARNING, formMsg)
                        try:
                            lock.acquire()
                            fp.write(formMsg + '\n')
                            lock.release()
                        except Exception, ex:
                            logger.log(CUSTOM_LOGGING.ERROR, ex)
                            if lock.locked():
                                lock.release()



    while conf.CRAWL_DEPTH >= currentDepth:

        links = Queue()
        # runThreads(conf.numThreads, crawlerThread)
        crawlerThread()
        visitSet = set()

        while links.qsize() > 0:
            tmpUrl = links.get()
            hashData = hashUrl(tmpUrl)
            if hashData not in visited and hashData not in visitSet:
                visitQueue.put(tmpUrl)
                visitSet.add(hashData)

        currentDepth += 1
    fp.close()
