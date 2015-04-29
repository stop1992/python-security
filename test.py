#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os

def test(*args):
	print args

def test2(**kwargs):
	# print kwargs


if __name__ == '__main__':
	os.system('printf "\033c"')

	a = ['a', 'b', 'c']
	b = {'abc':'test', 'cde':'lkdjl'}

	test(*a)
	test(**b)


