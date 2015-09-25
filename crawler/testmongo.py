#!/usr/bin/env python
# encoding: utf-8

import pymongo
import os
import calendar

def test1():
    connection = pymongo.MongoClient("localhost", 27017)
    db = connection.test
    table = db.test
    try:
        table.remove({'id':3})
    except InvalidDocument:
        print 'no field'
    table.insert({'id':3, 'value':{'20140501':1, '20140502':2}})
    data = table.find_one({'id':3})
    print data
    print '------------------------------------------------------------'
    date = '20140501'
    update = {"$set": {} }
    update['$set']['value.' + date] = 1
    print type(update['$set']['value.' + date])
    # table.find_one_and_update({'id':3}, update)
    data = table.find_one({'id':3})
    print type(data)
    print data['value'][date]
    # print data

class Mongo:
    def prepare(self):

        self.years = ['2013', '2014']
        self.months = []
        self.days = dict.fromkeys(self.years, [0])
        for i in xrange(1, 13):
            month = str(i)
            if len(month) != 2:
                month = '0' + month
            self.months.append(month)

        for y in self.years:
            for m in xrange(1, 13):
                day = calendar.monthrange(int(y), m)[1]
                # if len(day) != 2:
                    # day = '0' + day
                self.days[y].append(day)

    def list_plus(self, list_one, list_two):
        list_three = []
        list_length = len(list_one)
        for i in xrange(list_length):
            list_three.append(list_one[i] + list_two[i])
        return list_three

    def test2(self):

        self.prepare()
        client = pymongo.MongoClient("localhost", 27017)
        db = client.guba_data
        # table = db.db000003
        table = db.db000866
        list_length = len(open('keywords.txt', 'r').readlines())
        key_words_sum = [0] * list_length
        post_sum = 0
        for year in self.years:
            # date = year
            for month in self.months:
                # date = date + '-' + month
                for day in xrange(1, int(self.days[year][int(month)]) + 1):
                    day = str(day)
                    if len(day) != 2:
                        day = '0' + day
                    date = year + '-'  + month + '-' + day
                    result = table.find_one({'ask_time':date})
                    if result:
                        # print 'data in ', date , result['key_words'][1]
                        # print type(result['key_words'][1])
                        key_words_sum = self.list_plus(key_words_sum, result['key_words'])
                        post_sum += result['post_times']
        print 'key_words_sum: ', key_words_sum
        print 'post sum: ', post_sum
        fp = open('keys.txt', 'w')
        fp.write(str(key_words_sum))
        fp.close()


if __name__ == "__main__":
    os.system('printf "\033c"')

    mongo = Mongo()
    mongo.test2()
