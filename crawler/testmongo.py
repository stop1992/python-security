#!/usr/bin/env python
# encoding: utf-8

import pymongo
import os

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

if __name__ == "__main__":
    os.system('printf "\033c"')

    test1()
