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
        print 'year: ', self.years
        print 'month: ', self.months
        print 'dary: ', self.days

    def test2(self):

        self.prepare()
        client = pymongo.MongoClient("localhost", 27017)
        db = client.guba_data
        table = db.db000003
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
                        print 'data in ', date , result['key_words'][0]
                    else:
                        print 'There is no data in ', date
                    raw_input('please enter....')


if __name__ == "__main__":
    os.system('printf "\033c"')

    mongo = Mongo()
    mongo.test2()
