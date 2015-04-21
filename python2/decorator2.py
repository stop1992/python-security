# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os


def demo(func):
    print 'before myfunc called'
    func()
    print 'after myfunc called'
    return func


@demo
def myfunc():
    print 'called myfunc func'


os.system('printf "\033c"')

print '--------------------------------------------------'
myfunc()
print '---------------------------------------------------'
myfunc()
