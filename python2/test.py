#!/usr/bin/env python

#print "\033c"

计算离开打飞机
text = "1447932441@qq.com"
print "test"
print text.find('gmail')

if text.find('gmail') != -1:
	print "gmail"
else:
	if text.find('qq') != -1:
		print "qq mail"
	else: 
		print "no mail"
