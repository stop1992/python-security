# -*- encoding:utf-8 -*-

import os
import re
import xlrd
import xlwt
import types

class Handle(object):
	#def __init__(self):
		#pass

	def get_mrna_data(self):
		fp = open('mRNA.txt', 'r')
		# just get first line data 
		firstline = fp.readline()
		rna_data  = firstline.split('>')[1]
		self.len_rna = len(rna_data)
		# data formar: 
		# [ ['char', count], ['char', count], ...]
		self.mrna = []
		for i in xrange(self.len_rna):
			m = []
			self.mrna.append(m)
			self.mrna[i].append(rna_data[i])
			self.mrna[i].append(0)
			del m
		print self.mrna


	def handle_first_gene(self):
		dir_name = './testone/'
		for file_name in os.listdir(dir_name):
			print file_name
			pattern = re.compile(r'mRNA: NM_000927:  (\d+)~(\d+)')
			for line in open(dir_name+file_name, 'r'):
				result = pattern.match(line)
				if result != None:
					start = int(result.group(1)) - 1
					end = int(result.group(2))
					for i in xrange(start, end):
						self.mrna[i][1] += 1
			#print self.mrna
			#raw_input('press any key to continue')
		first_xlsl_file = xlwt.Workbook()
		table = first_xlsl_file.add_sheet('sheet1')
		for i in xrange(self.len_rna):
			table.write(i, 0, self.mrna[i][0])
			table.write(i, 1, self.mrna[i][1])
		first_xlsl_file.save('ENST00000449361.xls')

	def handle_second_gene(self):
		pass

	def handle_third_gene(self):
		pass

if __name__ == '__main__':
	os.system('printf "\033c"')

	handle = Handle()
	handle.get_mrna_data()
	handle.handle_first_gene()

