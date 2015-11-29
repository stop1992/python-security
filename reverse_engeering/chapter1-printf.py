#!/usr/bin/env python
# encoding: utf-8

import os
from ctypes import *

def test_cdll():
    libc = CDLL('libc.so.6')
    message_string = 'Hello world!'
    libc.printf('Testing: %s', message_string)

if __name__ == '__main__':
    os.system('clear')

    test_cdll()
