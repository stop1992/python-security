#!/usr/bin/env python

import email, imaplib
from pprint import pprint
import sys
import os
import base64
import chardet
from email.parser import Parser
import getpass

# Clear screen
os.system('printf "\033c"')

def connectimap():
	host = "imap.163.com"
	host = "imap.gmail.com"
	#host = "imap.qq.com"
	#username = "pdmtestmail@163.com"
	#passwd = "testtest"
	#username = "daitaomail@163.com"
	username = "daitaomail@gmail.com"
	passwd = "daitaoDAITAO68"
	#username = "1447932441@qq.com"
	#passwd = "daitaoDAITAO^^^^68"
	#username = "pdmtestmail@163.com"
	#passwd = getpass.getpass()


	imapins = imaplib.IMAP4_SSL(host)
	try:
		imapins.login(username, passwd)
	except imaplib.IMAP4.error:
		print "login error"
		sys.exit(1)
	return imapins

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
				print "content_html: "
				print content_html
				html = open("mail.html", "w")
				html.write(repr(content_html))
				html.close()
			if typ == 'text/plain':
				content_txt = part.get_payload(decode=True)
				content_txt = content_txt.decode('utf-8','ignore').encode('gbk','ignore')
				print "\033[22;31m enter text/plain part\033[1;m"
				#print "content_txt:"
				#print content_txt
				txt = open("mail.txt", "w")
				txt.write(repr(content_txt))
				txt.close()

def myunicode():
	return sys.stdout.encoding
	
def getheaderinfo(msg):
	mycode = myunicode()

	# parse subject
	try:
		sub = email.Header.decode_header(msg['Subject'])
	except email.errors.HeaderParseError:
		print "No Subject"
		sub = None
	if sub != None:
		if sub[0][1] == None:
			print "Subject: ", unicode(sub[0][0], mycode)
		else:
			print "Subject: ", unicode(sub[0][0], sub[0][1])



    # parse from
	fr = email.Header.decode_header(msg['From'])
	#print "len from: ", len(fr)
	#print fr[0] 
	tmpstr = fr[0][0]
	indexclrf = tmpstr.find("\r\n", 1)
	suffix_addr = tmpstr[indexclrf+3:]
	if indexclrf == 0:
		pass
	else:
		tmpstr = tmpstr[0:indexclrf]
		tmpstr = email.Header.decode_header(tmpstr[0:indexclrf])
		#print "Tmpstr: ", tmpstr
		paseafter = ''
		if tmpstr[0][1] == None:
			encode = chardet.detect(tmpstr[0][0])
			encoding = encode['encoding']
			parseafter = unicode(tmpstr[0][0], encoding, 'ignore')
		else:
			parseafter = unicode(tmpstr[0][0], tmpstr[0][1])
		#print "Parse after: ", parseafter

	encode = chardet.detect(fr[0][0])
	encoding = encode['encoding']
	frominfo = unicode(fr[0][0], encoding, 'ignore')

	#if fr[0][1] == None:
	#	frominfo = unicode(fr[0][0])
	#else:
	#	frominfo = unicode(fr[0][0], fr[0][1])

	if len(fr) > 1:
		frominfo += " " + fr[1][0]
	if indexclrf != -1:
		print "From: " , parseafter ,suffix_addr
	else:
		print "From: ", frominfo

	print "To: ", msg['To']
	print "\n\n\n"
	
def readmail(con):
	#typ, data = con.list()
	#for dt in data:
	#	print dt

	# data is numbers of message
	typ, data = con.select(mailbox='INBOX', readonly=True)
	#typ, data = con.select(mailbox = 'Sent Messages', readonly=True)
	#for num in data:
	#	print num

	# data is list number of message
	#typ, data = con.search(None, 'ALL')
	typ, data = con.search(None, 'ALL')
	#print "enter readmail"
	print data
	for msg_num in data[0].split():
		typ, dt = con.fetch(msg_num, '(BODY[])')
		msg = email.message_from_string(dt[0][1])
		getheaderinfo(msg)
		#parsemail(msg)
		#raw_input("press any key to continue")
		

if __name__ == '__main__':
	con = connectimap()
	readmail(con)
