#!/usr/bin/env python
#encoding:utf-8

from Queue import Queue
from bs4 import BeautifulSoup
import urlparse
import time

from lib.core.data import logger
from lib.core.data import conf
from lib.core.threads import runThreads
from lib.utils.userAgents import randomUserAgents
from thirdparty import requests


def crawler(target):

    visited = set()
    visitQueue = Queue()
    visitQueue.put(target)
    currentDepth = 0

    while conf.crawlDepth >= currentDepth:

        links = []
        while visitQueue.qsize() > 0:
            url = visitQueue.get()
            try:
                if url not in visited:
                    out_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print "[{out_time}] crawling {url}".format(out_time=out_time, url=url)
                    response = requests.get(url)
                    visited.add(url)

            except Exception, ex:
                print ex

            link = []
            soup = BeautifulSoup(response.text, 'lxml')
            for a in soup.find_all('a'):
                href = a.get('href')
                # if href and target in href:
                link.append(href)

            for i in link:
                links.append(i)

        for j in links:
            if j not in visited:
               visitQueue.put(j)

        currentDepth += 1
