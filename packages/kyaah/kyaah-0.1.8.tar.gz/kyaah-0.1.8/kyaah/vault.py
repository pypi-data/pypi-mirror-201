# -*- coding: utf-8 -*-
import os
from . import BaseMail


class Vault(BaseMail):
  """
  This class handle environment variable information
  
  use this class if you want to access your `mail address` and `password/app_password` from environment variable, all what you need is to put your `mail address environment variable` in place of your email address, likewise the password/app_password
  """
  
  @property
  def from_usr_addr(self):
    """get sender mail address from environment variable"""
    return os.environ.get(self.from_usr)
    
    
  @property
  def mail_passwd_env(self):
    """get sender mail password/app_password from environment variable"""
    return os.environ.get(self.mail_passwd)
