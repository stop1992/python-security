#!/usr/bin/env python
# encoding: utf-8

if __name__ == '__main__':

    total = 0

    with open('names.txt') as fp:

        total = sum(1 for i in fp)

    print total
