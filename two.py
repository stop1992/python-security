#!/usr/bin/env python
import one

def func():
	print "this is in two.py"

print "top-level in two.py"

if __name__ == "__main__":
	print "two is being run directly"
else:
	print "two is being imported into module"
