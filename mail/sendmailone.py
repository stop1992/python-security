#!/usr/bin/env python
import smtplib
import time
import getpass

sender = "daitaomail@gmail.com"
receiver = "daitaomail@163.com"
msg = """this mail is a test mail
		"""
host = "smtp.gmail.com"
port = "587"
print "test mail"
smtpserver = smtplib.SMTP(host, 587)
print "connecting server"
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(sender, getpass.getpass())
print "connect server success"
while 1:
    print "sending mail..."
    smtpserver.set_debuglevel(1)
    smtpserver.sendmail(sender, receiver, msg)
    print "mail send success"
    time.sleep(10)
