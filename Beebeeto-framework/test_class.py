#!/usr/bin/env python
# encoding: utf-8

import os

class Test:
    @classmethod
    def one(cls):
        print 'this is one func'

    @classmethod
    def two(cls):
        cls.one()
        print 'this is two func'


def main():

    test = Test()
    # test.one()
    test.two()

if __name__ == '__main__':
    os.system('clear')

    main()
