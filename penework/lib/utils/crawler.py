#!/usr/bin/env python
#encoding:utf-8

from Queue import Queue
from bs4 import BeautifulSoup
import urlparse
import time
import re
from threading import Lock

from lib.core.data import logger
from lib.core.data import conf
from lib.core.data import kb
from lib.core.enums import CUSTOM_LOGGING
from lib.core.common import findPageForms
from lib.core.threads import runThreads
from lib.utils.userAgents import randomUserAgents
from thirdparty import requests


def crawler(target):

    visited = set()
    # in_queue = Queue()
    visitQueue = Queue()
    visitQueue.put(target)
    currentDepth = 0
    fp = open('/home/xinali/python/penework/visited.txt', 'w')
    lock = Lock()


    def crawlerThread():

        while visitQueue.qsize() > 0:
            url = visitQueue.get()
            try:
                if url not in visited:
                    response = requests.get(url, timeout=10)
                    logger.log(CUSTOM_LOGGING.SYSINFO, 'crawled ' + url)
                    content = response.text
                    kb.pageEncoding = response.encoding
                    lock.acquire()
                    visited.add(url)
                    fp.write(url + '\n')
                    lock.release()
            except Exception, ex:
                # print ex
                continue
                # sys.exit(logger.log(CUSTOM_LOGGING.ERROR, 'get reponse error')

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

                        if href:
                            href = urlparse.urljoin(conf.scope, href)
                            links.put(href)

                except Exception, ex:  # for non-HTML files
                    print ex
                    continue
                finally:
                    # if conf.forms:
                    current = url
                    forms = findPageForms(content, current, False, True)
                    for form in forms:
                        logger.log(CUSTOM_LOGGING.WARN, 'form: ' + form)


    while conf.crawlDepth >= currentDepth:

        links = Queue()
        runThreads(conf.numThreads, crawlerThread)
        while links.qsize() > 0:
            j = links.get()
            if j not in visited:
               visitQueue.put(j)

        print 'currentdepth:', currentDepth
        print 'qsize:', visitQueue.qsize()

        currentDepth += 1
    fp.close()


        # for i in xrange(conf.crawlDepth):

            # if conf.numThreads:
                # runThreads(numThreads, crawlThread, threadChoice=(i>0))
            # else:
                # logger.log(CUSTOM_LOGGING.ERROR, 'the num of threads is not defined')
                # raise PeneworkGenericException('the num of threads is not defined')
