#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, generators, print_function, unicode_literals
from ..base import Base, Email
import os
from ..exception import *
import numbers


class SenderKeywords(Base):

	def create_new_email(self):
		Base.email = Email()

	def set_email_text(self, *sentences):
		sentences = [str(_) if (isinstance(_, numbers.Number)) else _ for _ in sentences]
		if Base.email is not None:
			Base.email.text = "\n".join(sentences)
		else:
			raise EmailNotFoundException("Use 'Create New Email' keyword first!")

	def set_email_subject(self, subject):
		if Base.email is not None:
			Base.email.subject = subject
		else:
			raise EmailNotFoundException("Use 'Create New Email' keyword first!")

	def add_attachment(self, paths):
		attachments = []
		for path in paths:
			full_path = self._get_source(path)
			if os.path.isfile(full_path):
				attachments.append(full_path)
			else:
				raise FileNotFoundException("Invalid path! File not found!")
			if Base.email is not None:
				Base.email.attachment = attachments
			else:
				raise EmailNotFoundException("Use 'Create New Email' keyword first!")

	def send_email_to(self, address):
		address = ";".join(address)
		Base.send(address)
