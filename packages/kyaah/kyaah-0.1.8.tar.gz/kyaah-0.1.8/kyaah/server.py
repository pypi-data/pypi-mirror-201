# -*- coding: utf-8 -*-
server = {
  "gmail": {
    "server": ["smtp.gmail.com"],
    "port": [465]
  },
  
  "local": {
    "server": ["localhost"],
    "port": [1025]
  },
  
  "yahoo": {
    "server": ["smtp.mail.yahoo.com", "pop.mail.yahoo.com", "imap.mail.yahoo.com"],
    "port": [465, 587, 995, 993]
  }
}

"""
port 995 is for yahoo pop server
port 993 is for yahoo imap server
"""


class Serve:
  """this class handle SMTP server suffs"""
  def mail(mail):
    return server[mail]
