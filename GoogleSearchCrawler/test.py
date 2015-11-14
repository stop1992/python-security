#!/usr/bin/env python
# encoding: utf-8

import os
import re
from collections import OrderedDict


def trans_data_headers(raw_data):
    raw_data = """GET /search?safe=strict&biw=1477&bih=782&q=intext:test&oq=intext:test&gs_l=serp.3...1025216.1028150.2.1034027.11.9.0.0.0.0.0.0..0.0....0...1c.1.64.serp..11.0.0.5h6vR50O-1I&bav=on.2,or.&bvm=bv.107406026,d.d24&fp=f21f2f8ad92d7e6d&tch=1&ech=1&psi=Cv1DVrb9K8fSUanGr9AN.1447296273010.5 HTTP/1.1
    Host: www.google.com.hk
    User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate
    DNT: 1
    Referer: https://www.google.com.hk
    Cookie: PREF=ID=1111111111111111:FF=2:LD=zh-CN:TM=1447296224:LM=1447296226:V=1:S=uLNKRThUqHchrNDn; NID=73=jMOtb7xjRQcoMiiRvc0Lq5ZIH0Vog96gizIdv4idGBLqtxa08HC1ChbwLc22TMJ8F4HUm2jotYNMTJltMsV-YWm3uA4FLS1h0piuSTf7-oZKEdzzQigrT5COMdnIcwjHbzIi7pKwZiGGRw92WR6mSO0hEEOgZKcigFx20W2yoR0CCg_D545nEQVG
    Connection: keep-alive
    """
    payload_headers = re.split('\n', raw_data)
    # datas = OrderedDict()
    datas = {}
    headers = {}
    for i in xrange(len(payload_headers)):
        if len(payload_headers[i]) > 4:
            if i == 0:
                data_all = re.split('\?| ', payload_headers[i])[2].split('&')
                for data in data_all:
                    data = data.split('=')
                    key = data[0]
                    value = data[1]
                    datas[key] = value
            else:
                header = payload_headers[i].split(': ')
                key = header[0].strip()
                value = header[1].strip()
                headers[key] = value
    return datas, headers


if __name__ == '__main__':
    os.system('clear')

    trans_data_headers()
