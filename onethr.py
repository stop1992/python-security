#!/usr/bin/env python

from time import ctime, sleep
import os
import thread


def loop0():
    print 'start loop 0 at:', ctime()
    sleep(4)
    print 'end loop 0 at:', ctime()


# print

def loop1():
    print 'start loop 1 at:', ctime()
    sleep(2)
    print 'end loop 0 at:', ctime()


def main():
    print 'starting at:', ctime()
    #loop0()
    #loop1()
    thread.start_new_thread(loop0, ())
    thread.start_new_thread(loop1, ())
    sleep(4)
    print 'all Done at:', ctime()


if __name__ == '__main__':
    os.system('printf "\033c"')
    main()
