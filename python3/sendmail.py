#!/usr/bin/env python

import smtplib
import sys
import getpass
from email.message import Message


smtpserver = "smtp.163.com"
user = "pdmtestmail@163.com"
toAddr = "1447932441@qq.com"

passwd = getpass.getpass()

text = """Hello, daitao
I am the pdmtestmail@163.com
This mail is a test to test some libs
				--dt"""

# try:
server = smtplib.SMTP_SSL(smtpserver)
#except smtplib.ConnectionRefusedError:
#	print "connect server error"
#	sys.exit(1)

msg = Message()
msg['Subject'] = "test mail"
msg['From'] = "pdmtestmail@163.com"
msg['To'] = "1447932441@qq.com"
msg.set_payload(text)

try:
    server.login(user, passwd)
except smtp.SMTPAuthenticationError:
    print ("smpt Authentication error")
    sys.exit(1)
else:
    #server.sendmail(user, toAddr, msg)
    server.send_message(msg, user, toAddr)  #new in python 3.2
finally:
    server.quit()
