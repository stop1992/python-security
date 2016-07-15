# encoding:utf-8

import xlrd
import os
from redis import Redis
import Queue
import re
import requests

def get_stock_num():
    Stock_queue = Queue.Queue()
    data = xlrd.open_workbook('stocknum.xlsx')
    sheet = data.sheets()[3]
    nrows =  sheet.nrows
    for i in xrange(nrows):
         stock = sheet.cell(i, 0).value
         tmp_split = stock.split('.')
         if tmp_split:
             stock_num = tmp_split[0]
             if stock_num == '000002':
                 continue
             Stock_queue.put(stock_num)

    server = Redis(host='192.168.1.108')
    server.delete('stocks')
    posts_account = 0
    for i in xrange(50):
        stock_num = Stock_queue.get()
        posts_account += get_html_data(stock_num)
    print 'total posts: ', posts_account
        # server.sadd('stocks', stock_num)
    # server.save()
    # print server.scard('stocks')

def get_html_data(stock_num):
    url = 'http://guba.eastmoney.com/list,' + stock_num + ',f_1.html'
    response = requests.get(url)
    # print response
    pattern = re.compile(ur'共有帖子数 (\d+) 篇')
    result = pattern.search(response.text)
    num = 0
    if result:
        num = int(result.group(1))
    print 'stock_num:', stock_num, ' posts_num:', num
    return num
    # if num <= 500 and num >= 300:
        # print 'stock_num:', stock_num, ' posts_num:', num
        # raw_input('please enter')
    # Html_queue.put(num)


if __name__ == '__main__':
    os.system('printf "\033c"')

    get_stock_num()
