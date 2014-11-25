#!/usr/bin/env python

import imaplib
import ConfigParser
import os
from pprint import pprint
import re

def open_connection():
	host = "imap.163.com"
	#host = "imap.gmail.com"
	connect = imaplib.IMAP4_SSL(host)
	username = "pdmtestmail@163.com"
	#username = "daitaomail@gmail.com"
	passwd = "testtest"
	#passwd = "daitaoDAITAO68"

	connect.login(username, passwd)
	return connect

def parse_list_response(line):
	rule = re.compile(r'\((.*?)\) "(.*?)" (.*)')
	flags, delimiter, mailbox_name = rule.match(line).groups()
	mailbox_name = mailbox_name.strip('"')
	return (flags, delimiter, mailbox_name.decode('UTF-8', 'ignore').encode('gbk'))


if __name__ == "__main__":
	c = open_connection()
	
	try:
		# test list() and status function
		#typ, data = c.list()#pattern="test")
		#for line in data:
			#print 'Response code:', typ
			#print 'Response:', parse_list_response(line)
			#flags, delimiter, mailbox_name = parse_list_response(line)
			#print c.status(mailbox_name, '(MESSAGES RECENT UNSEEN UIDVALIDITY)')
		typ, data = c.select('INBOX')
		print typ, data
		print "Message has %d"  % int(data[0])

	finally:
		c.logout
