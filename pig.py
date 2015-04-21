# -*- encoding:utf-8 -*- 

import xlrd
import os
import collections
import xlwt

class HandleStock:
	def __init__(self):
		pass

	def get_priceret_data(self):
		data = xlrd.open_workbook('priceret.xlsx')
		self.price_sheets = data.sheets()

	def get_stkcd_data(self):
		data = xlrd.open_workbook('stkcd.xls')
		self.stkcd_sheets = data.sheets()
		for stkcd_sheet in self.stkcd_sheets:
			pass

	def handle_data(self):
		self.stocks = []
		for sheet in self.price_sheets:
			stock = collections.defaultdict(list)
			# get total row number
			total_rows = sheet.nrows
			for row_number in xrange(total_rows):
				row_data = sheet.row_values(row_number)
				month = int(row_data[1].split('-')[1]) # yyyy-mm
				# every month data as a list
				#month_data = []
				#month_data.append(month + 10)
				#month_data.append(row_data[2])
				#stock[str(int(row_data[0]))].append(month_data)
				stock[str(int(row_data[0]))].append(month+10)
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
				stkcd_col_data = stkcd_sheet.col_values(j)
				for cell_data in stkcd_col_data:
					if cell_data == '':
						continue
					cell_data = str(int(cell_data))
					out_put = self.stocks[i][cell_data]
					save_excel_sheet.write(line, 0, cell_data.strip())
					for k in xrange(11, 23):
						try:
							index = out_put.index(k)
							save_excel_sheet.write(line, k - 10, out_put[index+1])
						except ValueError:
							save_excel_sheet.write(line, k - 10, ' ')
							continue
					line += 1
				line += 1
			i += 1
			year += 1
		save_excel.save('handled.xls')

if __name__ == '__main__':
	os.system('printf "\033c"')

	print 'start handle data....'
	handlestock = HandleStock()
	handlestock.get_priceret_data()
	handlestock.get_stkcd_data()
	handlestock.handle_data()
	print 'data handle finished'
