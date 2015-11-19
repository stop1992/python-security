#!/usr/bin/env python
# encoding: utf-8

from google import search
import os

def test_google():
    for url in search('intext:test', tld='com.tw', lang='cn', stop=20, pause=5.0):
        print url


if __name__ == '__main__':
    os.system('clear')

    test_google()
