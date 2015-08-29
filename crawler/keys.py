#!/usr/bin/env python
# encoding: utf-8

import os

def test():

    fp = open('keywords.txt', 'r')
    words = [ key.strip() for key in fp.readlines() ]
    print len(words)
    print type(words)

    for word in words:
        print word.strip()
        # print len(word)
        raw_input('please enter.....')

if __name__ == '__main__':
    os.system('printf "\033c"')

    test()
