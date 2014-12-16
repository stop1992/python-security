#!/usr/bin/env python 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

print "\033c"
from_add = "daitaomail@gmail.com"
to_add = "daitaomail@163.com"
msg = MIMEMultipart('alternative')
msg['Subject'] = "this a test mail"
msg['From'] = from_add
msg['To'] = to_add

text = "this is s test file"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""
part1 = MIMEMultipart(text, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)
username = "daitaomail@gmail.com"
passwd = "daitaoDAITAO68"
mail = smtplib.SMTP("smtp.gmail.com", 587)
mail.ehlo()
mail.starttls()
mail.login(username, passwd)
mail.set_debuglevel(1)
mail.sendmail(from_add, to_add, msg.as_string())
