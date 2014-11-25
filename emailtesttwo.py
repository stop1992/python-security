#!/usr/bin/env python
#!/bin/bash


import imaplib, getpass
import os
import email

os.system("rm -f mail.txt")
host = "imap.163.com"
username = "pdmtestmail@163.com"
#passwd = getpass.getpass()
passwd = "testtest"

imapinstance = imaplib.IMAP4_SSL(host)

imapinstance.login(username, passwd)

imapinstance.select("inbox", readonly = True)

typ, data = imapinstance.search(None, "UNSEEN")
print type(data)
print len(data)

for num in data[0].split():
	print num
	typ, data = imapinstance.fetch(num, '(RFC822)')
	content = 'Message %s\n%s\n' % (num, data[0][1])#.encode('utf-8').decode('gbk'))
	msg = email.message_from_string(data[0][1])
	content = msg.get_payload(decode=True)
	files = open("mail.txt", "a")
	files.write(repr(content))
	files.close()
imapinstance.close()
imapinstance.logout()

