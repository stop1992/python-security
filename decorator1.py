# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os

os.system('printf "\033c"')


def hello(func):
    def wrapper():
        print 'hello, %s' % func.__name__
        func()
        print 'goodby, %s' % func.__name__

    return wrapper


@hello
def foo():
    print 'i am foo'


foo()
