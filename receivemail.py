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

class Mail:

	def __init__(self, username):
		if username.find('qq') != -1:
			print "please enter passwd for qq mail"
			self.username = username
			self.passwd = getpass.getpass()
		elif username.find('gmail') != -1:
			print "please enter passwd for gmail"
			self.username = username
			self.passwd = getpass.getpass()
		else:
			print "please enter passwd for 163 mail"
			self.username = username
			self.passwd = getpass.getpass()

	def outputunicode():
		return sys.stdout.encoding

	def login(self, host):
		imapins = imaplib.IMAP4_SSL(host)
		try:
			imapins.login(self.username, self.passwd)
		except imaplib.IMAP4.error:
			print "login error"
			sys.exit(1)
		return imapins

	def readmail(con):
		#typ, data = con.list()
		#for dt in data:
		#	print dt

		# data is numbers of message
		typ, data = con.select(mailbox='INBOX', readonly=True)

		# data is list number of message
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
		
		def logout(imapins):
		imapins.close()
		imapins.logout()

	def parsemail(msg):
		for part in msg.walk():
			if part.is_multipart():
				#print part.get_content_type()
				continue
			else:
				typ = part.get_content_type()
				if typ == 'text/html': # don't parse for now
					pass
				if typ == 'text/plain':
					content_txt = part.get_payload(decode=True)
					coding = chardet.detect(content_txt)
					encoding = coding['encoding']
					content_txt = unicode(content_txt, encoding, 'ignore')
					print "email content text part:"
					print "-----------------------------------------------------------------------"
					print content_txt
					print "-----------------------------------------------------------------------"

if __name__ == '__main__':
	host_one = "imap.qq.com"
	host_two = "imap.163.com"
	host_three = "imap.gmail.com"

	username_one = "1447932441@qq.com"
	username_two = "daitaomail@gmail.com"
	username_three = "daitaomail@163.com"

	qqmail = Mail(username_one)
	gmail = Mail(username_two)
	mail163 = Mail(username_three)

	qqmail.login(host_one)
	gmail.login(host_two)
	mail163.login(host_three)
