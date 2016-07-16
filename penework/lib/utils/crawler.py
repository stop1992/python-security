#!/usr/bin/env python
#encoding:utf-8

from Queue import Queue


from penework.lib.core.data import logger
from penework.lib.core.threads import runThreads



def crawl(target):

    visit_queue = Queue()
    visited = set()
    scope = target


