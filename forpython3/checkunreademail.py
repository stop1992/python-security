#!/usr/bin/env python

import getpass, email, sys
from imapclient import IMAPClient

imapaddr = "imap.163.com"
username = "pdmtestmail@163.com"

#passwd = getpass.getpass()
passwd = 'testtest'
info = IMAPClient(imapaddr, ssl=True)

try:
	info.login(username, passwd)
except info.Error:
	print (username + "login error")
	sys.exit(1)
else:
	info.select_folder('INBOX', readonly = True)

result = info.search('UNSEEN')
msgdict = info.fetch(result, ['BODY.PEEK[]'])
for message_id, message in msgdict.items():
	mail = email.message_from_string(message['BODY[]'])

    # There maybe be chinese in subject and from, so decode
	subject = email.header.make_header(email.header.decode_header(mail['SUBJECT']))
	mailfrom = email.header.make_header(email.header.decode_header(mail['From']))

	mailcontent=""
    # Parase email content
	maintype = mail.get_content_maintype()
	if maintype == 'multipart':
		for part in mail.get_payload():
			if part.get_content_maintype == 'text':
				mailcontent = part.get_payload(decode=True).strip()
				print (len(mailcontent))
				input("Enter any key to continue...")
	elif maintype == 'text':
		maincontent = mail.get_payload(decode=True).strip()
		print (len(mailcontent))
		input("Enter any key to continue...")

	
	# Conver to chinese
	print ('New message')
	print ('From: ', mailfrom)
	print ('Subject: ', subject)
	print ('-'*10, "mailcontent", '-'*10)
	print (mailcontent.replace('<br>', '\n'))
	print ('-'*10, "mailcontent", '-'*10)

