# encoding:utf-8

import os
from redis import Redis
import Queue

def get_stock_num():
    Stock_queue = Queue.Queue()

    server = Redis(host='192.168.1.108')
    server.delete('stocks')
    posts_account = 0
    for stock_num in open('stocknums.txt', 'r'):
        stocknum = stock_num.strip()
        server.sadd('stocks', stocknum)
    print 'count:', server.scard('stocks')


if __name__ == '__main__':
    os.system('printf "\033c"')

    get_stock_num()
