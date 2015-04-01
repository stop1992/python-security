#-*- coding:utf-8 -*-
#!/usr/bin/env python

import re
import os

def get_data():
	fp = open('test.msd', 'r')
	data = fp.readlines()
	fp.close()
	for i in range(len(data)):
		data[i] = data[i].strip()
		if len(data[i]) > 50:
			data[i] = data[i].split()[1]
	iter_tmp = range(18, 17111, 66)

	first_line = []
	for i in iter_tmp:
		first_line.append(data[i])

	rest_line = []
	for i in iter_tmp:
		tmp_line = []
		tmp_line.append(i + 1)
		tmp_line.append(i + 64)
		rest_line.append(tmp_line)

	f = open('different.txt', 'w')
	line = 0
	for i in iter_tmp:
		tmp_j = range(rest_line[line][0], rest_line[line][1])	
		for j in tmp_j:
			if i == 17046:
				end = 59
			else:
				end = 60
			for k in range(0, end):
				try:
					if data[i][k] != data[j][k]:
						f.write(str(line*60+k+1) + ' ')
				except IndexError, e:
					print i
					print data[j+1]
					print len(data[i]), len(data[j])
					raw_input()
			f.write('\n')
		f.write('\n')
		f.write('----------------------------------------------------------------------------------------------------------------------------\n')
		line += 1	
	f.close()

if __name__ == '__main__':
	os.system('printf "\033c"')

	get_data()
