#!/usr/bin/env python
# encoding: utf-8

import os
from redis import Redis
from rq import Queue
import requests

from func import get_url


os.system('clear')
def main():
    q = Queue(connection=Redis())
    url = 'http://www.baidu.com'
    jobs = []
    for i in xrange(5000):
        job = q.enqueue_call(func=get_url, args=(url,), timeout=10000, result_ttl=10000)
        jobs.append(job)
        # print job.result



if __name__ == '__main__':

    main()
