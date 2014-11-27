#!/usr/bin/env python

import email, imaplib
from pprint import pprint
import os
import base64
import chardet
from email.parser import Parser

# Clear screen
os.system('printf "\033c"')

def connectimap():
	host = "imap.163.com"
	username = "pdmtestmail@163.com"
	passwd = "testtest"

	imapins = imaplib.IMAP4_SSL(host)
	imapins.login(username, passwd)
	return imapins

def showmail(data):
	if data.is_multipart():
		for part in data.get_payload():
			showmail(part)
	else:
		typ = data.get_content_charset()
		if typ == None:
			print data.get_payload()
		else:
			try:
				print unicode(data.get_payload('base64'), typ)
			except UnicodeDecodeError:
				print data

def check_content_type(msg):
	contenttype = msg.get_content_type()
	maintype = msg.get_content_maintype()
	subtype = msg.get_content_subtype()
	print "content/type: ", contenttype
	print "maintype: ", maintype
	print "subtype: ", subtype
	print "\n\n\n\n\n"

def getfilenameboundary(msg):
	filename = msg.get_filename()
	boundary = msg.get_boundary()
	print "filename: ", filename
	print "boundary: " , boundary
	print "\n\n\n\n"

def get_charset(msg):
	return msg.get_charset()

def parsemail(msg):
	p = Parser()
	for part in msg.walk():
		if part.is_multipart():
			if part.get_content_type() == 'multipart/alternative':
				content_html = part.get_payload(decode=True)
				print "open html files"
				html = open("mail.html", "w")
				html.write(repr(content_html))
				html.close()

def readmail(con):
	#typ, data = con.list()
	#for dt in data:
		#print dt

	# data is numbers of message
	typ, data = con.select(mailbox='INBOX', readonly=True)
	#for num in data:
	#	print num

	# data is list number of message
	typ, data = con.search(None, 'ALL')
	for msg_num in data[0].split():
		typ, dt = con.fetch(msg_num, '(BODY[])')
		msg = email.message_from_string(dt[0][1])
		parsemail(msg)
		raw_input("press any key to continue")
		

if __name__ == '__main__':
	con = connectimap()
	readmail(con)
