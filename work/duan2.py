# -*- encoding:utf-8 -*-

import os
import re
import xlrd
import xlwt
import types
import copy

CONTINUOUS_NUM = 15

class Handle(object):

	def get_mrna_data(self):
		data = xlrd.open_workbook('ABCB1.xlsx')
		self.data_sheets = data.sheets()
		# print type(self.data_sheets)

	def get_mrna_len(self):
		fp = open('mRNA.txt', 'r')
		self.mrna_seq = fp.readline()
		self.mrna_len = len(self.mrna_seq) - 1
		# print len(first_line)

	def handle_data(self):
		# handle every sheet
		sheet_nums = len(self.data_sheets)
		# count rna occur times
		self.mrna_count = [0] * self.mrna_len
		save_excel = xlwt.Workbook()
		for sheet in self.data_sheets:
			# get colums data, col = 1
			col_data = sheet.col_values(0)
			pattern = re.compile(r'mRNA: NM_000927:  (\d+)~(\d+)')
			result = pattern.findall(str(col_data))
			for item in result:
				# if seq occurs, count plus 1
				for i in xrange(int(item[0]) - 1, int(item[1])):
					self.mrna_count[i] += 1
			# store continuous sequence num
			self.continu_result = [0] * self.mrna_len
			start = 0
			end = 0
			# count every continuous sequence num
			continu_count = 0
			# count continus times
			continu_times = 0
			for i in xrange(self.mrna_len):
				if self.mrna_count[i] > CONTINUOUS_NUM:
					continu_count += 1
					if continu_count == 1:
						start = i
					if continu_count >= 7:
						end = i
				else:
					if continu_count >= 7:
						# continu_times as continu_result
						continu_times += 1
						for j in xrange(start, end+1):
							self.continu_result[j] = continu_times
					continu_count = 0
					start = 0
					end = 0

			if continu_count >= 7:
				# continu_times as continu_result
				continu_times += 1
				for j in xrange(start, end+1):
					self.continu_result[j] = continu_times
				continu_count = 0
				start = 0
				end = 0

			save_excel_sheet = save_excel.add_sheet(sheet.name, cell_overwrite_ok=True)
			for i in xrange(self.mrna_len):
				# write sequence num to excel
				save_excel_sheet.write(i, 0, i)
				# write sequence char to excel
				save_excel_sheet.write(i, 1, self.mrna_seq[i])
				# write count to excel
				save_excel_sheet.write(i, 2, self.mrna_count[i])
				# write continuous times result
				save_excel_sheet.write(i, 3, self.continu_result[i])
			save_excel_sheet.write(self.mrna_len, 0, 'pieces:'+str(continu_times))
			print 'pieces:', continu_times
		save_excel.save('result.xls')	

if __name__ == '__main__':
	os.system('printf "\033c"')

	handle = Handle()
	handle.get_mrna_len()
	handle.get_mrna_data()
	handle.handle_data()
