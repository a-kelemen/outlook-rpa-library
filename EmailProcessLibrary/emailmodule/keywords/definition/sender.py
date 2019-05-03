#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, generators, print_function, unicode_literals
from ..base import Base, Email
import os
from ..exception import *
import win32com.client as win32


class SenderKeywords(Base):

	def create_new_email(self):
		Base.email = Email()

	def set_email_text(self, *sentences):
		if Base.email is not None:
			#Base.email.text = " ".join(["as", "sadfsa"])
			#print(sentences)
			Base.email.text = "\n".join(sentences)
			#print("email.text: ")
			#print(Base.email.text)
			#pass
		else:
			raise EmailNotFoundException("Use Create New Email first!")

	def set_email_subject(self, subject):
		if Base.email is not None:
			Base.email.subject = subject
		else:
			raise EmailNotFoundException("Use Create New Email first!")

	def add_attachment(self, paths):
		attachments = []
		for path in paths:
			full_path = self._get_source(path)
			if os.path.isfile(full_path):
				attachments.append(full_path)
			else:
				#TODO exception szoveg
				raise FileNotFoundException("invalid path")
			if Base.email is not None:
				Base.email.attachment = attachments
			else:
				raise EmailNotFoundException("Use Create New Email first!")

	def send_email_to(self, address):
		#if type(address) is tuple:
		address = ";".join(address)
		Base.send(address)
