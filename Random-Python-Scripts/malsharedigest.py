# Open and catalog list of samples observed for a given date
# on Malshare.com, location: http://www.malshare.com/daily/malshare.current.txt
# To Do:
# [x] Create output file (csv or txt?)
# [x] Store each md5 as a csv with 'hash' : 'date' mapping
# [x] Add 'search' argument that searches result file for provided hash
import urllib2
import argparse
import csv
from sys import argv
from datetime import datetime, date
import re

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search",
	help="Search the consolidated results file for a hash")
parser.add_argument("-p", "--pull", action="store_true",
	help="Pull the most recent Malshare digest")
if len(argv) < 2:
	parser.print_help()
args = parser.parse_args()
found = False
if (args.pull):
	mal_digest = urllib2.urlopen(url='http://www.malshare.com/daily/malshare.current.txt')
	mal_digest = list(mal_digest)
	pull_time = [str(date.today())] * len(mal_digest) 
	strip_list = [x.strip('\n') for x in mal_digest]
	dictionary = dict(zip(strip_list, pull_time))
	writer = csv.writer(open('dictresults.csv', 'a'))
	for key, value in dictionary.items():
		writer.writerow([key, value])

elif (args.search):
	# Check to see if the param passed is a valid hash
	validity_check = re.compile(r'(?=(\b[A-Fa-f0-9]{32}\b))')
	if validity_check.match(args.search) == None:
		print "That isn't a md5 sum."
		exit()
	elif validity_check.match(args.search):
		with open('dictresults.csv', 'r') as f:
			reader = csv.reader(f)
			for num, row in enumerate(reader):
				if args.search in row[0]:
					print "%s was seen on %s" % (row[0], row[1])
					found = True
	if found != True:
		print "Sorry, we don't have that hash."
