#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('../')
import os
from penework.thirdparty.termcolor.termcolor import cprint


if __name__ == '__main__':
    os.system('clear')

    cprint('test', 'red')
    cprint('test', 'white')


