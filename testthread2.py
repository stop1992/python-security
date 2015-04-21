# -*- conding:utf-8 -*-
#!/usr/bin/env python

import time
import os
import threading

loops = [4, 2]


def loop(nloop, nsec):
    print 'starting loop', nloop, 'at:', time.ctime()
    time.sleep(nsec)
    print 'end loop', nloop, 'at:', time.ctime()


def main():
    print 'starting main at:', time.ctime()
    nloops = range(len(loops))
    threads = []
    for i in nloops:
        tmp = threading.Thread(target=loop,
                               args=(i, loops[i]))
        threads.append(tmp)

    for i in nloops:
        threads[i].start()
    #threads[i].join()
    #for i in nloops:
    print 'Main func done at', time.ctime()


if __name__ == '__main__':
    os.system('printf "\033c"')
    main()

