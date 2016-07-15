#!/usr/bin/env python
# encoding: utf-8

import multiprocessing
import os
from pymongo import MongoClient
from redis import Redis
import re

process_nums = multiprocessing.cpu_count()

class Multiprocess(multiprocessing.Process):

    MONGO_SERVER = '192.168.1.108'
    MONGO_PORT = 27017
    MONGO_DB_IN = 'guba_data'
    MONGO_DB_OUT = 'guba'
    REDIS_SERVER = '192.168.1.108'
    REDIS_PORT = 6379

    def prepare(self):

        # process_nums =  cpus - 1
        self.process_nums = multiprocessing.cpu_count()
        self.redis_client = Redis(self.REDIS_SERVER, self.REDIS_PORT)
        self.mongo_client =  MongoClient(self.MONGO_SERVER, self.MONGO_PORT)
        self.mongo_db_in = self.mongo_client[self.MONGO_DB_IN]
        self.mongo_db_out = self.mongo_client[self.MONGO_DB_OUT]
        # strip, then unicode, then compile
        self.key_words = [ re.compile(unicode(key.strip(), 'utf-8')) for key in open('keywords.txt', 'r').readlines() ]

        self.redis_client.sadd('stocks', '000002')
        self.redis_client.sadd('stocks', '000003')
        self.redis_client.sadd('stocks', '000866')

    def add(x, y):
        return x + y

    def store2mongo(self, stock_num, ask_time, key_words_accouts):
        post = self.mongo_db_out.stock_num
        # first get key words, then plus them ,then store
        all_document = post.find_one({'ask_time':ask_time})
        # exist ask_time data
        if all_document:
            key_words_accouts_before = all_document['key_words']
            post_times = all_document['post_times']
            # compute every day key words occur times
            # key_words_accouts_after = self.list_plus(key_words_accouts, key_words_accouts_before)
            key_words_accouts_after = map(key_words_accouts, key_words_accouts_before)
            # find key words, then update
            post.update_one({'ask_time':ask_time}, {'$set':{'key_words':key_words_accouts_after, \
                    'post_times':post_times+1}})
        else:    # not exist ask_time data
            post.insert({'ask_time':ask_time, 'post_times':1, 'key_words':key_words_accouts})
        print stock_num, ask_time, ' data process successfully....'

    def handle_data(self, stock_num):
        # stock num represent a collection
        table = self.mongo_db_in.stock_num
        if table:
            print 'start to process data....'
            for post in table.find():
                # get post ask time
                ask_time = post['ask_time']
                # store key words occur times
                key_words_accouts = []
                # this day present occur 1 time
                replys_data = post['replys_data']
                for pattern in self.key_words:
                    # initial find_count is 0
                    key_find_count = 0
                    for text in replys_data:
                        result = pattern.findall(text)
                        if result:
                            key_find_count = len(result)
                    key_words_accouts.append(key_find_count)
                # ready to store data to mongo_out
                print 'ready to store data.....'
                self.store2mongo(stock_num, ask_time, key_words_accouts)

    def run(self):
        print 'child process ', os.getpid(), ' starting....'
        while self.redis_client.scard('stocks') >= 0:
            # use a set to store stock nums
            stock_num = self.redis_client.spop('stocks')
            if stock_num:
                stock_num = 'db' + stock_num
                self.handle_data(stock_num)

if __name__ == '__main__':
    os.system('printf "\033c"')

    jobs = []
    for i in xrange(process_nums - 1):
        process = Multiprocess()
        process.prepare()
        print 'prepare done.....'
        jobs.append(process)
        process.start()
