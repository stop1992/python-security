# encoding:utf-8

# This Python file uses the following encoding: utf-8
#!/usr/bin/python
import urllib2,time,random

useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
cookie = '__jsluid=1cd45d882bd03dcfcf2b7526ccc31330; csrftoken=nAufgTbaSu12lZJSXB3UlFgZA5ftEP30; __jsl_clearance=1449561755.385|0|SEFgVOhKf%2BwQgoK7OtHCXw5tZi4%3D; Hm_lvt_e58da53564b1ec3fb2539178e6db042e=1447471265; Hm_lpvt_e58da53564b1ec3fb2539178e6db042e=1449561774'

def http_get(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-agent',useragent)
        req.add_header('Cookie',cookie)
        res = urllib2.urlopen(req)
        html = res.read()
        return html

    except Exception, e:
        if str(e).find('403') != -1:
            print '403'
            time.sleep(60)
            return http_get(url);
        return '-1'

def searcher(keyword,page):

        url = "https://www.zoomeye.org/search?q=" + keyword + "&p=" + str(page)
        ret = http_get(url)

        if ret == '-1':
            return ret
        if ret.find("flypig") == -1:
            return '-2'
        if ret.find("没有找到结果") != -1:
            return '0'
        if ret.find("您无权查看该页") != -1:
            return '-3'

        ret = ret.split('<ul class="result',1)[1]
        list = ret.split('<li>')
        rets = []

        for i in xrange(0,15):
            try:
                item = list[i]
                ip = item.split('ip:',1)[1]
                ip = ip.split('"',1)[0]
                rets.append(ip)
            except Exception, e:
                continue
        return rets

def main():

        f = open('result.txt','a+')

        for i in xrange(1,50):

            print 'getting page ', i

            ret = searcher('country:"Hongkong" port:6379',i);
            if ret == '-1':
                print ret
                break
            if ret == '-2':
                print '没有找到结果'
                break
            if ret == '-3':
                print '您无权查看该页'
                break
            if len(ret) < 1:
                continue

            for x in xrange(0,len(ret)):
                f.write(ret[x] + '\n')
            print ret

        f.close()
        print 'done'

if __name__ == '__main__':
        main()

