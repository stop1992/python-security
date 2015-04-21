#!/usr/bin/env python

import os


def main(a, b, **kwargs):
    print 'this is main func'
    print a, b
    print kwargs


def test():
    print 'this test func'


if __name__ == '__main__':
    os.system('printf "\033c"')
    apply(main, (1, 2), {'x': '1', 'y': '2'})

