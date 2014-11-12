#!/usr/bin/env python

def func():
	print "this is one.py"

print "top-level in one.py"

if __name__ == "__main__":
	print "one.py is being run directly"
else:
	print "one.py is being imported into another module"
