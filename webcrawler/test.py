import xlrd
import os

if __name__ == '__main__':
	os.system('printf "\033c"')

	data = xlrd.open_workbook('data.xls')
	table = data.sheets()[0]
	colums = table.col_values(1)

	for item in colums:
		if item:
			print item
			raw_input('press')
