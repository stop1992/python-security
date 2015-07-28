# encoding:utf-8

import os 

if __name__ == '__main__':
	os.system('printf "\033c"')

	while True:
		chars = raw_input('please enter ch: ')
		if chars == 'exit':
			break
		urlresult = ''
		for ch in chars:
			tmp_hex = hex(ord(ch))
			urlresult += '%' + tmp_hex[2] + tmp_hex[3]
		print urlresult + '\n'
