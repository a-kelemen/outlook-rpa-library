#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, generators, print_function, unicode_literals
from ..base import Base
import datetime
import os
import pythoncom

from ..exception import *


class ReaderKeywords(Base):

	def read_last_received_email(self):
		inbox = Base._get_inbox_folder()
		messages = inbox.Items
		messages.Sort("[ReceivedTime]", True)
		# print("utolso email bodyja:")
		# print("utolso email ideje:" + str(messages[0].ReceivedTime))
		# print(Base._get_sentences(messages[0].Body))
		return Base._get_sentences(messages[0].Body)

	def read_last_email_from(self, sender_address):
		inbox = Base._get_inbox_folder()
		messages = inbox.Items
		messages.Sort("[ReceivedTime]", True)
		for mail in messages:
			if sender_address == mail.SenderEmailAddress:
				# print(Base._get_sentences(mail.Body))
				return Base._get_sentences(mail.Body)
		return None

	def last_received_subject_should_be(self, subject):
		inbox = Base._get_inbox_folder()
		messages = inbox.Items
		messages.Sort("[ReceivedTime]", True)
		last_subject = Base._get_sentences(messages[0].Subject)
		last_subject = last_subject[0]
		if last_subject != subject:
			#raise AssertionError(subject + str("!=") + last_subject)
			raise AssertionError("Subject of last received mail is: '" + last_subject + "', not '" + subject + "'!")
		#TODO logger
		# else:
		# 	print(subject + str("==") + last_subject)

	def last_sent_subject_should_be(self, subject):
		sent_folder = Base._get_sent_folder()
		messages = sent_folder.Items
		messages.Sort("[CreationTime]", True)
		last_subject = Base._get_sentences(messages[0].Subject)
		last_subject = last_subject[0]
		if last_subject != subject:
			#raise AssertionError(subject + str("!=") + last_subject)
			raise AssertionError("Subject of last sent mail is: '" + last_subject + "', not '" + subject + "'!")
		#TODO logger
		# else:
		# 	print(subject + str("==") + last_subject)

	def get_email(self, sender, subject, date_from, date_to):
		try:
			#date_from = datetime.date(date_from)
			datetime_from = datetime.datetime.strptime(date_from, '%Y.%m.%d')
		except Exception:
			#print("Exception: :" + e.__class__.__name__)
			#raise ValueError("The date_from parameter is not valid in Get Email keyword!")
			raise ValueError(str(date_from) + "does not match format '%Y.%m.%d'")
		if date_to is None:
			datetime_to = datetime.datetime.now()
		else:
			try:
				datetime_to = datetime.datetime.strptime(date_to, '%Y.%m.%d') + datetime.timedelta(days=1)
			except Exception:
				#print("Exception: :" + e.__class__.__name__)
				#raise ValueError("The date_to parameter is not valid in Get Email keyword!")
				#raise ValueError(str(date_to) + "does not match format '%Y.%m.%d'")
				raise ValueError(str(date_to) + "does not match format '%Y.%m.%d'")
		inbox = Base._get_inbox_folder()
		messages = inbox.Items
		messages.Sort("[ReceivedTime]", True)
		messages = messages.Restrict("[ReceivedTime] >= '" + datetime_from.strftime('%m/%d/%Y %H:%M %p') + "'")
		messages = messages.Restrict("[ReceivedTime] < '" + datetime_to.strftime('%m/%d/%Y %H:%M %p') + "'")
		for mail in messages:
			if mail.Subject == subject and mail.SenderEmailAddress == sender:
				#print("get_mail: ", mail.Subject, mail.SenderEmailAddress, mail.ReceivedTime )
				return mail
			#print(mail.Subject, mail.ReceivedTime)
		#if sender_address == mail.SenderEmailAddress:
		#	print(Base._get_sentences(mail.Body))
		#	return Base._get_sentences(mail.Body)
		return None

	def save_attachments(self, email, save_folder):
		attachments = email.attachments
		for att in attachments:
			if save_folder == "default_":
				file_source = att.FileName
			else:
				file_source = os.path.join(save_folder, att.FileName)
			full_path = self._get_source(file_source)
			try:
				att.SaveASFile(full_path)
			except pythoncom.com_error:
				raise DirectoryNotFoundException(str("Directory doesn't exist: ") + save_folder)

	def get_email_text(self, email):
		return email.Body

	def get_email_subject(self, email):
		return email.Subject

	def get_email_time(self, email):
		return email.ReceivedTime

	def get_email_sender(self, email):
		return email.Sender.Address


