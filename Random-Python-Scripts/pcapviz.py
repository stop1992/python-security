#!/usr/bin/python

'''
Leverage scapy to visualize pcaps. 
Inspired by Sean T
Written by Blevene
'''

from scapy.all import *
import argparse

parser = argparse.ArgumentParser(description="Visualize a .pcap file using scapy and afterglow.")
parser.add_argument("-c", "--conversations", help="Use this to view a conversations summary.",
	action="store_true")
parser.add_argument("-a", "--afterglow", help="Use this to view a complete viz.",
	action="store_true")	
args = parser.parse_args()

if not len(sys.argv) > 1:
	print "Please use one of: -a, -c, or -h as an argument."

else:
	infile = raw_input('Please type an absolute path to the .pcap file: ')
	p=rdpcap(infile)
	print "Reading %s now." % infile
	
	
	if args.conversations:
		p.conversations()
		#[Documentation] https://github.com/d1b/scapy/blob/master/scapy/plist.py#L239
	elif args.afterglow:
		p.afterglow()
		#[Documentation] https://github.com/d1b/scapy/blob/master/scapy/plist.py#L264

print "Enjoy your visualization!"
