#!/usr/bin/env python
# encoding: utf-8

import redis
from pymongo import MongoClient
import os

def clear():
    client = redis.Redis(host='localhost', port=6379)
    request = client.get('guba:requests')
    if request == None:
        print 'guba:requests not exist...'
    else:
        client.delete('guba:requests')
        print 'delete guba:request successfully....'

    dupefilter = client.get('guba:dupefilter')
    if dupefilter:
        client.delete('guba:dupefilter')
        print 'delete guba:request successfully...'
    else:
        print 'guba:dupefilter not exist...'


if __name__ == '__main__':
    os.system('printf "\033c"')

    clear()
