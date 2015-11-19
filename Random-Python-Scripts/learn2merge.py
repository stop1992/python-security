# This script takes everything under each "digit" 
# and combines it onto one line

#######################
#Structure of the data
# 1
# line
# textone
# texttwo
# 2
# textthree
# linetwo
# 3
# somethingone
# somethingtwo
#######################
from sys import argv

file = argv[1]
data = open(file).readlines()
for n, line in enumerate(data):
	if line[0].isdigit():
		data[n] = "\n"+line.strip()
	else:
		data[n] = line.strip()

print ' '.join(data)
