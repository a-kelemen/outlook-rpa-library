#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, generators, print_function, unicode_literals
from ..base import Base
from ..exception import *


class LoginKeywords(Base):

	def should_be_logged_in_to_outlook(self, email_address):
		app = Base._get_outlook_app()
		accounts = app.Session.Accounts
		account_names = [_.DisplayName for _ in accounts]
		if email_address not in account_names:
			raise OutlookException(email_address + " user isn't logged in to Outlook. Logged in users: " + str(account_names))
