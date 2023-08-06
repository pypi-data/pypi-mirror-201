# -*- coding: utf-8 -*-
import imghdr
import logging
import smtplib
from email.message import EmailMessage

"""
  NOTSET    ---  0
  DEBUG     ---  10
  INFO      ---  20
  WARNING   ---  30  (default)
  ERROR     ---  40
  CRITICAL  ---  50
"""

formatter = "[+] [%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(format = formatter)

logger = logging.getLogger() # Creating an object
logger.setLevel(logging.DEBUG) # Setting the threshold of logger to DEBUG


class BaseMail:
  """
  The base class for mail
  Note:
    in all `BaseMail` mathod there is a keyword argument called `port`, that port is the port of your SMTP server which will listen, make sure to put the port that is convenient to your SMTP server e.g for gmail is 465, although kyaah has a dict tionary of server, where each server has a list of ports, SMTP server, etc.
  """
  
  def __init__(
    self,
    from_usr = None,
    to_usr = None,
    subject = None,
    body = None,
    mail_passwd = None,
    server = None,
    ):
    
    self.from_usr = from_usr
    self.to_usr = to_usr
    self.subject = subject
    self.body = body
    self.mail_passwd = mail_passwd
    self.server = server
    
    
    while self.from_usr == None:
      raise UnboundLocalError(f"`from_usr` is required")
    while self.to_usr == None:
      raise UnboundLocalError(f"`to_usr` is required")
    
  @property
  def from_usr_addr(self):
    """the sender mail address"""
    return self.from_usr
    

  @property
  def mail_passwd_env(self):
    """the sender mail password"""
    return self.mail_passwd
    

  @property
  def mail_msg(self):
    """content of the mail (subject and message body)"""
    subj = self.subject
    body = self.body
    data = f"Subject: {subj}\n\n{body}"
    return data
    

  def check_required(self):
    """checking for required values"""
    while self.mail_passwd == None:
      raise UnboundLocalError(f"`mail_passwd` is required")
    while self.server == None:
      raise UnboundLocalError(f"`server` is required")
      

  def mail_head(self, msg):
    """contains the sender, receiver and subject"""
    # grab the subject from `mail_msg` method by spliting it,
    # and grab the first index which is the subject,
    # then we slice the first index from index `9` that mean we negate
    # `subj` variable of mail_msg method of this class
    # which is `Subject: `
    msg['Subject'] = self.mail_msg.split('\n')[0][9:]
    msg['From'] = self.from_usr_addr
    msg['To'] = self.to_usr
    
    
  def mail_open(self, msg, port):
    """this open the connection, and login to email address using email address provided together with password/app_password"""
    with smtplib.SMTP_SSL(self.server, port) as smtp:
      smtp.login(self.from_usr_addr, self.mail_passwd_env)
      smtp.send_message(msg)
      
      
  def local_mail(self, port=1025):
    """localhost mail"""
    with smtplib.SMTP(self.server, port) as smtp:
      smtp.sendmail(self.from_usr_addr, self.to_usr, self.mail_msg)
      
      
  def send_mail(self, port=25):
    """send mail with ssl security"""
    
    """recepients is the list of receivers email address that you will send emaill address to, if the recepients is not included when call the method it will only send it to the `self.to_usr` that you pass in as the argument when instanciating the `BaseMail` class"""
    
    self.check_required()
    
    if len(self.to_usr) > 1:
      """if there is recepients"""
      for receiver in self.to_usr:
        with smtplib.SMTP_SSL(self.server, port) as smtp:
          smtp.login(self.from_usr_addr, self.mail_passwd_env)
          smtp.sendmail(self.from_usr_addr, receiver, self.mail_msg)
    elif len(self.to_usr) == 1:
      with smtplib.SMTP_SSL(self.server, port) as smtp:
        smtp.login(self.from_usr_addr, self.mail_passwd_env)
        smtp.sendmail(self.from_usr_addr, self.to_usr, self.mail_msg)
        

  def file_to_send(self, file_to, f_opration, _msg=None, maintype=None):
    # maintype = "image" for sending image
    # maintype = "application" for sending files like pdf
    
    if maintype == "application":
      with open(file_to, f_opration) as file_send:
        f_read = file_send.read()
        f_name = file_send.name
      _msg.add_attachment(f_read, maintype=maintype, subtype='octet-stream', filename=f_name)
    if maintype == "image":
      with open(file_to, f_opration) as img_send:
        img_read = img_send.read()
        f_type = imghdr.what(img_send.name)
        f_name = img_send.name
      _msg.add_attachment(img_read, maintype=maintype, subtype=f_type, filename=f_name)
      

  def mail_with_image(self, image, port=25):
    """send mail together with an image"""
    self.check_required()
    
    if len(self.to_usr) > 1:
      """if the list of to_usr is more than one"""
      for receiver in self.to_usr:
        msg = EmailMessage()
        msg['Subject'] = self.mail_msg.split('\n')[0][9:]
        msg['From'] = self.from_usr_addr
        msg['To'] = receiver
        msg.set_content(self.mail_msg.split('\n')[2])
        
        if type(image) == list:
          """send message with morethan one image"""
          
          for my_img in image:
            self.file_to_send(my_img, "rb", _msg=msg, maintype="image")
          self.mail_open(msg, port)
        elif type(image) == str:
          """send message with one image"""
          
          self.file_to_send(image, "rb", _msg=msg, maintype="image")
          self.mail_open(msg, port)
        else:
          logger.error(f"only list or string can be pass as argument in {self.mail_with_image}")
    elif len(self.to_usr) == 1:
      msg = EmailMessage()
      self.mail_head(msg)
      msg.set_content(self.mail_msg.split('\n')[2])
      
      if type(image) == list:
        """send message with morethan one image, for only one destination"""
        
        for my_img in image:
          self.file_to_send(my_img, "rb", _msg=msg, maintype="image")
        self.mail_open(msg, port)
      elif type(image) == str:
        """send message with one image, for only one destination"""
        
        self.file_to_send(image, "rb", _msg=msg, maintype="image")
        self.mail_open(msg, port)
      else:
        logger.error(f"only list or string can be pass as argument in {self.mail_with_image}")
        

  def mail_with_file(self, mail_files, port=25):
    """send mail together with a list of mail_files"""
    self.check_required()
    
    msg = EmailMessage()
    self.mail_head(msg)
    msg.set_content(self.mail_msg.split('\n')[2])
    
    for a_file in mail_files:
      self.file_to_send(a_file, "rb", _msg=msg, maintype="application")
    self.mail_open(msg, port)
    
    
  def mail_with_page(self, file=None, port=25):
    """send mail with html page. You can pass a keyword args of `file='default'` which will send a default html page provided within this class method, that is for test
    
    But if you want to send yor own html page assign the `file` with a value of the absolute location of your html page"""
    
    self.check_required()
    
    msg = EmailMessage()
    self.mail_head(msg)
    msg.set_content(self.mail_msg.split('\n')[2])
    
    if file == 'default':
      dummy_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <h1 style="color:SlateGray;">Hello world mail from {self.from_usr_addr}</h1>
  <p style="color:brown;">Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum voluptate ipsum voluptatum doloribus, incidunt totam doloremque quae quibusdam exercitationem sapiente vel veritatis consequuntur earum et. Quod nobis minus minima repellat.</p>
</body>
</html>
"""
      msg.add_alternative(dummy_page, subtype='html')
    elif file != None:
      with open(file) as f_html:
        html_f = f_html.read()
      msg.add_attachment(html_f, subtype='html')
    self.mail_open(msg, port)
