#!/usr/bin/env python

print "\033c"

text = "abcdabcdabcd"
index = text.find("cd")
print "index: ", index
while index != -1:
	print index
	tmpstr = text[0:index+1]

	text = text[index+1:]
	print text
	print "tmpstr: ", tmpstr
	index = text.find("d")
	raw_input("Press any key to continue")
