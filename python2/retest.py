#!/usr/bin/env python

import re
import os

if __name__ == "__main__":
	os.system('printf "\033c"')

	f = open('data.txt', 'r')
	s = f.readlines()
	data = s[0] 
	patt = '.+?(\d+-\d+-\d+)'
	m = re.match(patt, data)
	#m = re.search(patt, data)
	print m.group(1)
