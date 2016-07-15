#!/usr/bin/env python
# encoding: utf-8

import multiprocessing
import os
from pymongo import MongoClient
from redis import Redis
import re
import time

from clear import drop_mongo

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

redis_client.sadd('stocks', '000002')
redis_client.sadd('stocks', '000866')

def add(x, y):
    return x + y

def store2mongo(stock_num, ask_time, key_words_accouts):
    post = mongo_db_out[stock_num]
    # first get key words, then plus them ,then store
    all_document = post.find_one({'ask_time':ask_time})
    # exist ask_time data
    if all_document:
        key_words_accouts_before = all_document['key_words']
        post_times = all_document['post_times']
        # compute every day key words occur times
        key_words_accouts_after = map(add, key_words_accouts, key_words_accouts_before)
        # find key words, then update
        post.update_one({'ask_time':ask_time}, {'$set':{'key_words':key_words_accouts_after, \
                'post_times':post_times+1}})
    else:    # not exist ask_time data
        post.insert({'ask_time':ask_time, 'post_times':1, 'key_words':key_words_accouts})
    # print stock_num, ask_time, ' data process successfully....'

def handle_data(stock_num):
    # stock num represent a collection
    table = mongo_db_in[stock_num]
    if table:
        # print 'start to process data....'
        for post_day in table.find():
            # get post ask time
            ask_time = post_day['ask_time']
            # store key words occur times
            key_words_accouts = []
            # this day present occur 1 time
            replys_data = post_day['replys_data']

            for pattern in key_words:
                # initial find_count is 0
                key_find_count = 0
                for text in replys_data:
                    result = pattern.findall(text)
                    if result:
                        key_find_count = len(result)
                key_words_accouts.append(key_find_count)
            # store2mongo(stock_num, ask_time, key_words_accouts)
            post = mongo_db_out[stock_num]
            # first get key words, then plus them ,then store
            all_document = post.find_one({'ask_time':ask_time})
            # exist ask_time data
            if all_document:
                key_words_accouts_before = all_document['key_words']
                post_times = all_document['post_times']
                # compute every day key words occur times
                key_words_accouts_after = map(add, key_words_accouts, key_words_accouts_before)
                # find key words, then update
                post.update_one({'ask_time':ask_time}, {'$set':{'key_words':key_words_accouts_after, \
                        'post_times':post_times+1}})
            else:    # not exist ask_time data
                post.insert({'ask_time':ask_time, 'post_times':1, 'key_words':key_words_accouts})


def handle(process_name):
    while redis_client.scard('stocks') > 0:
        # use a set to store stock nums
        stock_num = redis_client.spop('stocks')
        if stock_num:
            stock_num = 'db' + stock_num
            handle_data(stock_num)

def main():
    jobs = []
    pools = multiprocessing.Pool()
    for i in xrange(process_nums - 1):
        process_name = 'process_' + str(i)
        pools.apply_async(handle, (process_name, ))
    pools.close()
    pools.join()

if __name__ == '__main__':
    os.system('printf "\033c"')

    start = time.time()
    print 'start time: ', start
    main()
    end = time.time()
    print 'used time: ', end - start
    # drop_mongo()
    # test()
