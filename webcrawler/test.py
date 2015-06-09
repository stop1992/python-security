#-*- encoding:utf-8 -*-

import xlrd
import os

if __name__ == '__main__':
	os.system('printf "\033c"')

	# data = xlrd.open_workbook('data.xls')
	# table = data.sheets()[0]
	# colums = table.col_values(1)

	a = ['test', 'wangxi', 123, 'daitao']
	b = 'test wangxi haha hello world daitao'
	for item in a:
		if b.find(str(item)) > 0:
			print item, 'in b'
	# for item in colums:
		# if item:
			# print item
			# raw_input('press')
