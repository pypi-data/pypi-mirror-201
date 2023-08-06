# -*- coding: utf-8 -*-
import json
import math
import random
import logging
import geocoder
import requests


formatter = "[+] [%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(format = formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Tokens:
  """The base class for OTP mail"""
  
  def mail_otp(self, _range=6):
    """send otp code"""
    digits = "0123456789"
    OTP = ""
    for _ in range(_range):
      OTP += digits[math.floor(random.random()*10)]
    return OTP
    

class Faker:
  """a class that give you random email address"""
  
  _source = ["https://www.guerrillamail.com/ajax.php?f=get_email_address&ip=", "&agent=Mozilla_foo_bar"]
  
  def __init__(self, url=_source, ip="me"):
    self.url = url
    self.ip = ip
    
    
  def what_ip(self):
    """find ip address of the requester"""
    g = geocoder.ip(self.ip).raw
    ip = g.get("ip")
    return ip
    
    
  @property
  def make_request(self):
    """this method make a request along side with an ip address from `what_ip` method of this class"""
    url_first = self.url[0]
    url_mid = self.url[1]
    url_end = self.what_ip()
    
    com_url = url_first + url_end + url_mid
    r = requests.get(com_url).text
    return r
    
    
  def faker(self) -> dict:
    """give the actual maill address generated from guerrillamail"""
    gue_raw = json.loads(self.make_request)
    _fake = gue_raw["email_addr"]
    return {"fake_email": _fake}
