# -*- encoding:utf-8 -*-

import os
import xlrd
import xlwt
import collections

class Handle(object):

	def get_stkcd_data(self):
		data = xlrd.open_workbook('stkcd2.xls')
		self.stkcd_sheets = data.sheets()

	def get_priceret_data(self):
		data = xlrd.open_workbook('priceret2.xlsx')
		self.price_sheets = data.sheets()


	def handle_data(self):
		self.stocks = []
		for sheet in self.price_sheets:
			stock = collections.defaultdict(list)
			# get total row number
			total_rows = sheet.nrows
			for row_number in xrange(total_rows):
				row_data = sheet.row_values(row_number)
				month = int(row_data[1].split('-')[1]) # yyyy-mm
				stock[str(int(row_data[0]))].append(month)
				stock[str(int(row_data[0]))].append(row_data[2])
			self.stocks.append(stock)
			stock = None

		year = 2004
		i = 0
		save_excel = xlwt.Workbook()
		for stkcd_sheet in self.stkcd_sheets:
			line = 0
			save_excel_sheet = save_excel.add_sheet(str(year), cell_overwrite_ok=True)
			for j in xrange(6):
				""" write data to file with "s" style"""
				column = 1
				stkcd_col_data = stkcd_sheet.col_values(j)
				for cell_data in stkcd_col_data:
					if cell_data == '':
						break
					cell_data = str(int(cell_data))
					save_excel_sheet.write(line, column, cell_data) # write stock code
					line += 1

					for date in xrange(1, 13):
						save_excel_sheet.write(line, 0, str(year)+'/'+str(date))
						line += 1

					line -= 12 # back January

					out_put = self.stocks[i][cell_data]

					for k in xrange(1, 13):
						try:
							index = out_put.index(k)
							save_excel_sheet.write(line, column, out_put[index+1])
						except ValueError:
							save_excel_sheet.write(line, column, ' ')
						finally: # right or wrong, line must plus 1
							line += 1
					line -= 13 # back stock code line
					column += 1
				line += 13
			i += 1
			year += 1
		save_excel.save('handled2.xls')


if __name__ == '__main__':
	os.system('printf "\033c"')

	handle = Handle()
	handle.get_stkcd_data()
	handle.get_priceret_data()
	handle.handle_data()
