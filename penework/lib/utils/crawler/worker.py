#!/usr/bin/env python
# encoding: utf-8
from redis import Redis
from rq import Queue, Connection, Worker


def main():

    with Connection():
        qs = ['default']
        w = Worker(qs)
        w.worker()


