#!/usr/bin/env python
# encoding: utf-8

import os
import requests

import gevent.monkey
gevent.monkey.patch_all()

from gevent.pool import Pool


class VerifyShellshock(object):
    def __init__(self):
        self.fuzzing = ['/cgi-bin/load.cgi',
                '/cgi-bin/gsweb.cgi',
                '/cgi-bin/redirector.cgi',
                '/cgi-bin/test.cgi',
                '/cgi-bin/index.cgi',
                '/cgi-bin/help.cgi',
                '/cgi-bin/about.cgi',
                '/cgi-bin/vidredirect.cgi',
                '/cgi-bin/click.cgi',
                '/cgi-bin/details.cgi',
                '/cgi-bin/log.cgi',
                '/cgi-bin/viewcontent.cgi',
                '/cgi-bin/content.cgi',
                '/cgi-bin/admin.cgi',
                '/cgi-bin/webmail.cgi']

    def use_zmap_scan(self):
        cmd_80 = 'zmap -B 20M -p 80 100.0.0.0/8 200.0.0.0/8 300.0.0.0/8 -o result.txt'
        cmd_8080 = 'zmap -B 20M -p 8080 100.0.0.0/8 200.0.0.0/8 300.0.0.0/8 -o result.txt'
