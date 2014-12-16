#!/usr/bin/env python

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import smtplib
filename = "sendmailone.py"
f = file("sendmailone.py", "rb")
from_add = "daitaomail@gmail.com"
to_add = "daitaomail@gmail.com"

username = from_add
passwd = getpass.getpass()

# handle header info
msg = MIMEMultipart('alternative')
msg['Subject'] = "this email with a attachment"
msg['From'] = from_add
msg['To'] = to_add

# handle attachment info
attachment = MIMEText(f.read())
attachment['Content-Type'] = 'application/octet-stream'
attachment['Content-Disposition'] =  "attachment; filename=sendmailone.py"
msg.attach(attachment)

mail = smtplib.SMTP("smtp.gmail.com", 587)
mail.ehlo()
mail.starttls()
mail.login(username, passwd)
mail.set_debuglevel(1)
mail.sendmail(from_add, to_add, msg.as_string())
mail.quit()
