# -*- encoding: utf-8 -*-

import os
import re
import requests
import codecs
import time


if __name__ == '__main__':
    os.system('printf "\033c"')

    # start = time.clock()
    start = time.time()
    # for i in xrange(10000):
    a = []
    a = [u'代涛', u'王喜', u'daitao', u'wangxi']
    b = u'代涛 王喜 wangxi daitao'
    for item in a:
        print item
        pattern = re.compile(item)
        result = pattern.findall(b)
        if result:
                for i in result:
                        print i, 'in b'
                # print result
        # print item
        # if b.find(item) > 0:
                # print item, 'in b'
    """
    try:
            response = requests.get('http://guba.eastmoney.com/list,000002,f_1.html')
            pattern = re.compile(ur'共有帖子数 (\d+) 篇')
            result  = pattern.search(response.text)
            # print type(result)
            num = int(result.group(1))
            print num, type(num)
    except Exception, e:
                    print str(e)
            # print 'get error'
            """
