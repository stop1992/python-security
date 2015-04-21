#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import xlrd
import os

if __name__ == '__main__':
	os.system('printf "\033c"')

	data = xlrd.open_workbook('stkcd.xls')
	sheets = data.sheets()[0]
	for i in xrange(1, 7):
		print sheets.col_values(i)
		raw_input('press')


