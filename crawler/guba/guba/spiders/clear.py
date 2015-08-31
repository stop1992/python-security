#!/usr/bin/env python
# encoding: utf-8

import redis
from pymongo import MongoClient
import os

def clear_mongodb():
    # mongo_server = '192.168.1.108'
    mongo_server = 'localhost'
    mongo_port = 27017
    client = MongoClient(mongo_server, mongo_port)
    db = client.guba_data
    if db:
        collections = 'db000866'
        db.drop_collection(collections)
        # client.drop_database('guba_data')
        # dropDatabase()
        print 'drop ', collections, 'successfully....'

def clear_redis():
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

def clear():
    clear_redis()
    clear_mongodb()

if __name__ == '__main__':
    os.system('printf "\033c"')

    clear()
