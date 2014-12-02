#!/usr/bin/env python

import email, imaplib
from pprint import pprint
import sys
import os
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
	#passwd = "daitaoDAITAO68"
	#username = "pdmtestmail@163.com"
	#passwd = getpass.getpass()


	imapins = imaplib.IMAP4_SSL(host)
	#imapins = imaplib.IMAP4(host)
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
			#print part.get_content_type()
			continue
		else:
			typ = part.get_content_type()
			if typ == 'text/html': # don't parse for now
				pass
				#print "This email content is a html file"
				#content_html = part.get_payload()
				#print type(content_html)
				#print content_html
				#content_html = content_html.decode('utf-8', 'ignore').encode('gbk','ignore')
				#print "content_html: "
				#print content_html
				#html = open("mail.html", "w")
				#html.write(content_html)
				#html.close()
				#raw_input("just pause")
			if typ == 'text/plain':
				content_txt = part.get_payload(decode=True)
				coding = chardet.detect(content_txt)
				encoding = coding['encoding']
				content_txt = unicode(content_txt, encoding, 'ignore')
				print "email content text part:"
				print "-----------------------------------------------------------------------"
				print content_txt
				print "-----------------------------------------------------------------------"

def outputunicode():
	return sys.stdout.encoding
	
def getheaderinfo(msg):
	mycode = outputunicode()

	# parse subject
	sign = False # subject default is short
	try:
		sub = ''
		sub = email.Header.decode_header(msg['Subject'])
	except email.errors.HeaderParseError:
		sub = '' 
		sign = True # subject is long
		subject = msg['Subject']
		#print type(subject)
		#print "len sub: ", len(subject)
		index = subject.find("?=")
		subject_one = subject
		while index != -1:
			partsub = subject_one[0:index+2]
			subject_one = subject_one[index+2:]
			tmpsub = email.Header.decode_header(partsub)
			sub += unicode(tmpsub[0][0], tmpsub[0][1])
			#print "part subject: ", partsub 
			#print "left subject: ", subject_one
			index = subject_one.find("?=")

	if sign == True:
		print "Subject: ", sub
	else:
		if sub[0][0] == 'None':
			print "Subject: No subject"
		else:
			if sub[0][1] == None:
				print "Subject: ", unicode(sub[0][0], mycode)
			else:
				print "Subject: ", unicode(sub[0][0], sub[0][1])

    # parse from
	fr = email.Header.decode_header(msg['From'])
	#print "len from: ", len(fr)
	#print fr[0] 
	tmpstr = fr[0][0]
	indexclrf = tmpstr.find("<")
	suffix_addr = tmpstr[indexclrf:]
	if indexclrf != -1:
		tmpstr = tmpstr[0:indexclrf-1].strip("\r\n\"") #excise some specification
		#print "Tmpstr: ", tmpstr
		tmpstr = email.Header.decode_header(tmpstr)
		paseafter = ''
		if tmpstr[0][1] == None:
			encode = chardet.detect(fr[0][0]) # get the text encoding
			encoding = encode['encoding']
			parseafter = unicode(tmpstr[0][0], encoding, 'ignore')
		else:
			parseafter = unicode(tmpstr[0][0], tmpstr[0][1])
		#print "Parse after: ", parseafter

	encode = chardet.detect(fr[0][0])
	encoding = encode['encoding']
	frominfo = unicode(fr[0][0], encoding, 'ignore')

	if len(fr) > 1: # if len > 2, then fromaddr is in fr[1][0]
		frominfo += " " + fr[1][0]
	if indexclrf != -1:
		print "From: " , parseafter ,suffix_addr
	else:
		print "From: ", frominfo

	print "To: ", msg['To']
	print "Date: ", msg['Date']
	
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
	typ, data = con.search(None, 'UNSEEN')
	msgnum = 1
	for msg_num in data[0].split():
		print "Message %s" % (msgnum)
		msgnum += 1
		typ, dt = con.fetch(msg_num, '(BODY[])')
		msg = email.message_from_string(dt[0][1])
		getheaderinfo(msg)
		parsemail(msg)
		print "\n"
		#raw_input("press any key to continue")

def logout(imapins):
	imapins.close()
	imapins.logout()

if __name__ == '__main__':
	con = connectimap()
	readmail(con)
	logout(con)
