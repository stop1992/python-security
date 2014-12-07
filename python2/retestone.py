#!/usr/bin/env python

import re
import os

#os.system("clear")

rule = re.compile(r'(.*?)')
text = '<p>test</p>'
text = 'abcgdefg'
data = rule.match(text)

print '------------------------'
#print length
#print len(data.groups())
print data.group(0)
print '------------------------'
