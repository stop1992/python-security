#!/usr/bin/env python

from email.message import Message
import email.utils

text = """ Hello, daitao
 This is a test mail
  --dt
"""
msg = Message()
msg['To'] = "1447932441@qq.com"
msg['From'] = "pdmtestmail@163.com"
msg['Subject'] = "this is a test mail"
msg['Date'] = email.utils.formatdate(localtime=1)
#msg['Message-ID'] = email.utils.make_msgid()
msg.set_payload(text)

print msg.as_string()
