#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, generators, print_function, unicode_literals
import win32com.client as win32

#from emailProcessLibrary.emailmodule import OutlookException
from .exception import *
import os
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class Email(object):

	def __init__(self):
		self.text = ""
		self.subject = ""
		self.attachment = None
		self.to = None

	def send(self, to, outlook_app):
		new_mail = outlook_app.CreateItem(0)
		# pontosvesszovel kell elvalasztani ha tobb nev is van elvileg
		#https: // stackoverflow.com / questions / 22681903 / send - email - to - multiple - recipients - using - win32com - module - in -python
		#newMail.To = 'Amy; john; sandy'
		if type(to) is list:
			to = ";".join(to)
		new_mail.To = to
		new_mail.Subject = self.subject
		new_mail.Body = self.text
		attachment = self.attachment
		new_mail.Attachments.Add(attachment)
		new_mail.Send()


class Base(object):

	email = None

	@staticmethod
	def _get_outlook_app():
		try:
			outlook_app = win32.Dispatch('outlook.application')
			return outlook_app
		except Exception as e:
			#TODO exception
			print("Exception: :" + e.__class__.__name__)
			raise OutlookException("Nincs futo, bejelentkezett outlook alkalmazas!")

	@staticmethod
	def _get_inbox_folder():
		app = Base._get_outlook_app()
		mapi = app.GetNamespace("MAPI")
		folders = mapi.Folders.Item(1)
		inbox = folders.Folders[1]
		#print(inbox.Name)
		return inbox

	@staticmethod
	def _get_sent_folder():
		app = Base._get_outlook_app()
		mapi = app.GetNamespace("MAPI")
		folders = mapi.Folders.Item(1)
		sent = folders.Folders[3]
		#print("---:" + sent.Name)
		return sent

	@staticmethod
	def _get_sentences(msg):
		msg_list = [_.rstrip() for _ in msg.split("\n") if _.strip() is not ""]
		return msg_list

	@staticmethod
	def send(address):
		outlook_app = Base._get_outlook_app()
		#app = win32.Dispatch('outlook.application')
		new_mail = outlook_app.CreateItem(0)
		new_mail.Body = Base.email.text
		new_mail.Subject = Base.email.subject
		#print("address: " + address)
		new_mail.To = address
		if Base.email.attachment is not None:
			for attachment in Base.email.attachment:
				new_mail.Attachments.Add(attachment)
		new_mail.Send()

	def _get_process_folder(self):
		try:
			process_dir = os.path.dirname(BuiltIn().get_variable_value("${SUITE SOURCE}"))
			return process_dir
		except RobotNotRunningError as e:
			base_dir = self._nth_parent_folder(__file__, 3)
			return os.path.join(base_dir, str("tests"))

	def _get_source(self, file_name):
		try:
			file_name = file_name.lstrip("\\").lstrip("/")
		except UnicodeDecodeError:
			pass
		if file_name == str("default_"):
			return self._get_process_folder()
		else:
			file_full_path = os.path.abspath(file_name)
			if not Base._is_absolute_path(file_name):
				return os.path.join(self._get_process_folder(), str(os.path.normpath(file_name)))
			else:
				return file_full_path

	def _nth_parent_folder(self, file_source, n):
		if n > 0:
			return self._nth_parent_folder(os.path.dirname(file_source), n-1)
		else:
			return file_source

	@staticmethod
	def _is_absolute_path(path):
		return os.path.normpath(path) == os.path.abspath(path)





