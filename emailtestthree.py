#!/usr/bin/env python

import email, imaplib
from pprint import pprint
import os

# Clear screen
os.system('printf "\033c"')

def connectimap():
	host = "imap.163.com"
	username = "pdmtestmail@163.com"
	passwd = "testtest"

	imapins = imaplib.IMAP4_SSL(host)
	imapins.login(username, passwd)
	return imapins

def readmail(con):
	#typ, data = con.list()
	#for dt in data:
		#print dt
	# data is numbers of message
	typ, data = con.select(mailbox='INBOX', readonly=True)
	#for num in data:
	#	print num
	#print type(data[0])
	#print data[0]
	# data is list number of message
	typ, data = con.search(None, 'ALL')
	#print type(data)
	for msg_num in data[0].split():
		#print type(num)
		#print num[0]
		#print "Message %s" % num
		#print type(msg_num)
		#print len(msg_num)
		typ, dt = con.fetch(msg_num, '(BODY[HEADER] BODY[TEXT] BODY[MIME])')
		print "---------------------------------"
		print len(dt)
		#print len(dt[0])
		#print "---------------------------------\n"
		#print dt[0][0]
		#print "+++++++++++++++++++++++++++++++++\n"
		#print dt[0][1]
		#print "---------------------------------"
		#print dt[1]
		#print "\n\n\n\n\n" + dt[1]

		#content = email.message_from_string(dt[0][1])
		#content = content.get_payload(decode=True)
		#print content
		#print content['Content']
		#print content['Subject']
		#input ("enter any key to continue")
		#print "Message %s" % msg_num
		#print "Message content"
		#pprint(dt)
		#print "Message content: %s" % dt

if __name__ == '__main__':
	con = connectimap()
	readmail(con)
