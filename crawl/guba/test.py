#!/usr/bin/env python
# encoding: utf-8

import os
import multiprocessing
from pymongo import MongoClient
from redis import Redis
import re

# process_nums = multiprocessing.cpu_count()

MONGO_SERVER = '192.168.1.108'
MONGO_PORT = 27017
MONGO_DB_IN = 'guba_data'
MONGO_DB_OUT = 'guba'
REDIS_SERVER = '192.168.1.108'
REDIS_PORT = 6379


# process_nums =  cpus - 1
process_nums = multiprocessing.cpu_count()
redis_client = Redis(REDIS_SERVER, REDIS_PORT)
mongo_client =  MongoClient(MONGO_SERVER, MONGO_PORT)
mongo_db_in = mongo_client[MONGO_DB_IN]
mongo_db_out = mongo_client[MONGO_DB_OUT]
# strip, then unicode, then compile
key_words = [ re.compile(unicode(key.strip(), 'utf-8')) for key in open('keywords.txt', 'r').readlines() ]



def test():
    print process_nums
    print redis_client
    print mongo_db_in

if __name__ == '__main__':
    os.system('printf "\033c"')

    test()
