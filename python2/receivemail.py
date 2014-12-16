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
			#self.passwd = getpass.getpass()
			self.passwd = "daitaoDAITAO68"
		else:
			print "please enter passwd for 163 mail"
			self.username = username
			#self.passwd = getpass.getpass()
			self.passwd = "daitaoDAITAO68"

	def outputunicode(self):
		return sys.stdout.encoding

	def login(self, host):
		imapins = imaplib.IMAP4_SSL(host)
		try:
			print self.username, self.passwd
			print host
			imapins.login(self.username, self.passwd)
		except imaplib.IMAP4.error:
			print "login error"
			return None;
		print "login success"
		return imapins

	def readmail(self, con):
		typ, data = con.list()
		for dt in data:
			print dt

		# data is numbers of message
		typ, data = con.select(mailbox='INBOX', readonly=False)

		# data is list number of message
		typ, data = con.search(None, "ALL")
		msgnum = 1
		for msg_num in data[0].split():
			print "Message %s" % (msgnum)
			msgnum += 1
			typ, dt = con.fetch(msg_num, '(BODY[])')
			#typ2, dt2 = con.fetch(msg_num, '(FLAGS)')
			typ3, dt3 = con.expunge()
			#print dt2
			print dt3
			msg = email.message_from_string(dt[0][1])
			self.getheaderinfo(msg)
			self.parsemail(msg)
			isdelete = raw_input("delete yes/no(please enter y/n):")
			print "isdelete: ", isdelete
			if isdelete == "y":
				print "deleting this message"
				con.store(msg_num, '+FLAGS', r'\Deleted')
				typ, response = con.expunge()
				print response
			print "\n"
			#raw_input("press any key to continue")
			
	def getheaderinfo(self, msg):
		mycode = self.outputunicode() # parse subject
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
		
	def logout(self, imapins):
		imapins.close()
		imapins.logout()

	def parsemail(self, msg):
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
	host_two = "imap.gmail.com"
	host_three = "imap.163.com"

	username_one = "1447932441@qq.com"
	username_two = "daitaomail@gmail.com"
	username_three = "daitaomail@163.com"

	#qqmail = Mail(username_one)
	#mail163 = Mail(username_three)
	#con_163 = mail163.login(host_three)
	#mail163.readmail(con_163)
	#mail163.logout()

	gmail = Mail(username_two)
	con_gmail = gmail.login(host_two)
	gmail.readmail(con_gmail)
	gmail.logout(con_gmail)
