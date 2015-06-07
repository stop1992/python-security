# encoding:utf-8

import xlrd
import os
from redis import Redis

def get_stock_num():
	data = xlrd.open_workbook('data.xls')
	table = data.sheets()[0]
	colum_data = table.col_values(1)
	
	server = Redis(host='192.168.1.108')
	for data in colum_data:
		server.sadd('stock_num', data)
	server.save()

if __name__ == '__main__':
	os.system('printf "\033c"')

	get_stock_num()
