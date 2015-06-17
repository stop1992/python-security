# -*- encoding:utf-8 -*-

import os
import re
import xlrd
import xlwt
import types
import copy

class Handle(object):

	def get_mrna_data(self):
		data = xlrd.open_workbook('ABCB1.xlsx')
		self.data_sheets = data.sheets()
		# print type(self.data_sheets)

	def handle_data(self):
		# handle every sheet
		sheet_nums = len(self.data_sheets)
		for sheet in self.data_sheets:
			# get colums data, col = 1
			col_data = sheet.col_values(0)
			pattern = re.compile(r'mRNA: NM_000927:  (\d+)~(\d+)')
			result = pattern.findall(str(col_data))
			print len(result)
			# print sheet.nrows
			

if __name__ == '__main__':
	os.system('printf "\033c"')

	handle = Handle()
	handle.get_mrna_data()
	handle.handle_data()
