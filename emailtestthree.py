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
	#username = "pdmtestmail@163.com"
	#passwd = "testtest"
	username = "daitaomail@163.com"
	passwd = "daitaoDAITAO68"

	imapins = imaplib.IMAP4_SSL(host)
	imapins.login(username, passwd)
	return imapins

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
	for part in msg.walk():
		if part.is_multipart():
			print part.get_content_type()
			continue
		else:
			typ = part.get_content_type()
			if typ == 'text/html':
				content_html = part.get_payload(decode=True)
				content_html = content_html.decode('utf-8', 'ignore').encode('gbk','ignore')
				#print "content_html: "
				#print content_html
				html = open("mail.html", "w")
				html.write(repr(content_html))
				html.close()
			if typ == 'text/plain':
				content_txt = part.get_payload(decode=True)
				content_txt = content_txt.decode('utf-8').encode('gbk','ignore')
				print "content_txt:"
				print content_txt
				txt = open("mail.txt", "w")
				txt.write(repr(content_txt))
				txt.close()

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
