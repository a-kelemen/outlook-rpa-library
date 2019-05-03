#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, generators, print_function, unicode_literals
from robot.api import logger
from .emailmodule.keywords.definition.login import LoginKeywords
from .emailmodule.keywords.definition.reader import ReaderKeywords
from .emailmodule.keywords.definition.sender import SenderKeywords


def keyword(name=None):
	#TODO ebbe az kell, hogy lefuttassa a keywordot, es ha sikres, akkor kiir valamit hogy sikeres hogy legyen
	#valami haszna
	if callable(name):
		logger.warn(str(name))
		#logger.warn("csaxsa")
		return keyword()(name)

	def _method_wrapper(func):
		func.robot_name = name
		return func
	return _method_wrapper

#TODO mi van ha tobb bejelentkezett felhasznalo van
#TODO ha nem vagyok bejelentkezve, akkor kiirja  hibat?
#TODO mas outlookon is mukodik?


class EmailProcessLibrary(object):
	"""EmailProcessLibrary is a process automation library for Robot Framework.

	Par keyword az outlook app automatizalasara windowson. Szoval kell hogy legyen aoutlook és
	egy bejelentkezett felhasznalo. Ha nics bejelentkezve akkor nem mukodik. Login keyword nincs mert akkor
	a password nem lenne biztonsagos.

	== Table of contents ==

	- `Sending Email`
	- `Shortcuts`
	- `Keywords`

	= Sending Email =

	This is a complete example for sending an email.


	``kiemeles``  `link`(neha kiemeles?)


	| `Click Element` | example | # Match based on ``id`` or ``name``.            |
	| `Click Link`    | example | # Match also based on link text and ``href``.   |
	| `Click Button`  | example | # Match based on ``id``, ``name`` or ``value``. |
	"""
	__version__ = '0.1.0'

	ROBOT_LIBRARY_SCOPE = 'GLOBAL'
	#TODO nem global kell hogy minden subprocessben uj email tudjunk csinalni. de lehett hogy global is jo
	ROBOT_LIBRARY_VERSION = __version__

	def __init__(self):
		self.reader = ReaderKeywords()
		self.sender = SenderKeywords()
		self.login = LoginKeywords()

	@keyword(name="Create New Email")
	def create_new_email(self):
		"""
		Creates a new, empty email.

		Initial keyword for sending emails, so it has to be called before setting email.

		Examples:
		| `Create New Email`  |                  | # Creates a new email without body, subject and attachment |
		| `Set Email Subject` |  sample_subject  | # After calling Create New Email, subject could be changed |
		| `Create New Email`  |                  | # Body, Subject and Attachment will be empty again         |
		| `Send Email To`     | sample@robot.com | # Sends an empty email                                     |

		For more examples see `Sending Email` section above.
		"""
		self.sender.create_new_email()

	@keyword(name="Set Email Text")
	def set_email_text(self, *lines):
		"""
		Sets the body of the email.

		Each *kwarg defines a row of the body.

		This keyword is dependent from keyword `Create New Email`.

		Examples:
		| `Create New Email`                | # Creates a new email without body, subject and attachment |
		| `Set Email Text`                  |                                                            |
		| ...  Hi!                          | # First line of the email.                                 |
		| ...  This is the text of the mail | # Second line of the email.                                |
		| ...  Best Regards,                | # Third line of the email.                                 |
		| ...  Robot                        | # Fourth line of the email.                                |

		For more examples see `Sending Email` section above.
		"""
		self.sender.set_email_text(*lines)

	@keyword(name="Set Email Subject")
	def set_email_subject(self, subject):
		"""
		Sets the subject of the email.

		This keyword is dependent from keyword `Create New Email`.

		Examples:
		| `Create New Email`  | # Creates a new email without body, subject and attachment |
		| `Set Email Subject` |                                                            |
		| ...  sample subject | # Sets the subject of the email                            |

		For more examples see `Sending Email` section above.
		"""
		self.sender.set_email_subject(subject)

	@keyword(name="Send Email To")
	def send_email_to(self, *address):
		"""
		Sends the email to the given address.

		This keyword is dependent from keyword `Create New Email`.

		Examples:
		| `Send Email To`   | robot1@robot.com | # Sends the previously created email to the given address   |
		| `Send Email To`   |                  |                                                             |
		| ...  r1@robot.com |                  |                                                             |
		| ...  r2@robot.com |                  | # Sends the previously created email to the given addresses |

		For more examples see `Sending Email` section above.
		"""

		self.sender.send_email_to(address)

	@keyword(name="Add Attachment")
	def add_attachment(self, *attachments):
		"""
		Adds ``attachments`` to the email.

		This keyword is dependent from keyword `Create New Email`.

		Examples:
		| `Create New Email`         | # Creates a new email without body, subject and attachment |
		| `Add Attachment`           |                                                            |
		| ...  C://folder//file1.txt |                                                            |
		| ...  C://folder//file2.txt | # Adds the attachments to the email.                       |

		For more examples see `Sending Email` section above.
		"""
		self.sender.add_attachment(attachments)

	@keyword(name="Read Last Received Email")
	def read_last_received_email(self):
		"""
		Returns the text of the last received email.

		Examples:
		| ${msg_body}= | `Read Last Received Email` | # The variable will contain the body of the last received email. |
		"""
		return self.reader.read_last_received_email()

	@keyword(name="Read Last Email From")
	def read_last_email_from(self, sender_address):
		"""
		Returns the text of the last email of the given `sender_address`.

		Examples:
		| ${msg_body}= | `Read Last Email From` | sender@robot.com | # The variable will contain the body of the last received email from sender@robot.com. |
		"""
		return self.reader.read_last_email_from(sender_address)

	@keyword(name="Last Received Subject Should Be")
	def last_received_subject_should_be(self, subject):
		"""
		Fails if the subject of the last received email is not the given `subject`.

		Examples:
		| `Last Received Subject Should Be` | subject1 | # Passes if the subject of the last received mail is subject1.   |
		| `Last Received Subject Should Be` | subject2 | # Fails if the subject of the last received mail isn't subject2. |
		"""
		self.reader.last_received_subject_should_be(subject)

	@keyword(name="Last Sent Subject Should Be")
	def last_sent_subject_should_be(self, subject):
		"""
		Fails if the subject of the last sent email is not the given `subject`.

		Examples:
		| `Last Sent Subject Should Be` | subject1 | # Passes if the subject of the last sent mail is subject1.   |
		| `Last Sent Subject Should Be` | subject2 | # Fails if the subject of the last sent mail isn't subject2. |
		"""
		self.reader.last_sent_subject_should_be(subject)

	@keyword(name="Get Email")
	def get_email(self, sender, subject, date_from="2000.01.01", date_to=None):
		"""
		Returns an email.

		- ``sender`` : The address of the sender.
		- ``subject`` : The subject of the mail.
		- ``date_from`` : Starting point of the time interval. Default value is 2000.01.01.
		- ``date_to`` : Endpoint of the time interval. Default value is today.

		``sender`` and ``subject`` parameters are mandatory.

		Required date format: _YYYY.MM.DD_

		Examples:
		| ${mail}= | `Get Email` | sender@mail.com | sample_sub |            |                    | # Returns the last email from sender@mail.com with sample_sub subject.                                       |
		| ${mail}= | `Get Email` | sender@mail.com | sample_sub | 2018.01.01 |                    | # Returns the last email from sender@mail.com with sample_sub subject from date 2018.01.01                   |
		| ${mail}= | `Get Email` | sender@mail.com | sample_sub | 2018.01.01 | date_to=2018.01.15 | # Returns the last email from sender@mail.com with sample_sub subject between date 2018.01.01 and 2018.01.15 |

		Returns the last email, which meets the given conditions.
		"""
		return self.reader.get_email(sender, subject, date_from, date_to)

	@keyword(name="Save Attachments")
	def save_attachments(self, email, save_folder="default_"):
		"""
		Saves the attachments of the given email to the given folder.

		Fails, if ``save_folder`` doesn't exist.

		Examples:
		| ${mail}=           | `Get Email` | sender@mail.com      | sample_sub |                                               |
		| `Save Attachments` | ${mail}     | ..//downloads//mails |            | # Saves the attachments to the emails folder. |
		"""
		self.reader.save_attachments(email, save_folder)

	@keyword(name="Get Email Text")
	def get_email_text(self, email):
		"""
		Returns the text of the given ``email``.

		Examples:
		| ${mail}= | `Get Email`      | sender@mail.com | sample_sub |                                                         |
		| ${text}= | `Get Email Text` | ${mail}         |            | # _${text}_ variable will contain the text of the mail. |
		"""

		return self.reader.get_email_text(email)

	@keyword(name="Get Email Subject")
	def get_email_subject(self, email):
		"""
		Returns the subject of the given ``email``.

		Examples:
		| ${mail}=    | `Get Email`         | sender@mail.com | sample_sub |                                                               |
		| ${subject}= | `Get Email Subject` | ${mail}         |            | # _${subject}_ variable will contain the subject of the mail. |
		"""
		return self.reader.get_email_subject(email)

	@keyword(name="Get Email Time")
	def get_email_time(self, email):
		"""
		Returns the delivery time of the given ``email``.

		Examples:
		| ${mail}= | `Get Email`      | sender@mail.com | sample_sub |                                                                  |
		| ${time}= | `Get Email Time` | ${mail}         |            | # _${time}_ variable will contain the delivery time of the mail. |
		"""
		return self.reader.get_email_time(email)

	@keyword(name="Get Email Sender")
	def get_email_sender(self, email):
		"""
		Returns the sender address of the given ``email``.

		Examples:
		| ${mail}=           | `Get Email`        | sender@mail.com | sample_sub |                                                                        |
		| ${sender_address}= | `Get Email Sender` | ${mail}         |            | # _${sender_address}_ variable will contain the address of the sender. |
		"""
		return self.reader.get_email_sender(email)

	@keyword(name="Should Be Logged In To Outlook")
	def should_be_logged_in_to_outlook(self, email_address):
		"""
		Fails if the email of the logged in user isn't identical with the given ``email_address``.

		Examples:
		| `Should Be Logged In To Outlook` | robot@mail.com | # Passes if robot@mail.com is logged in to Outlook   |
		| `Should Be Logged In To Outlook` | human@mail.com | # Fails if human@mail.com isn't logged in to Outlook |
		"""
		self.login.should_be_logged_in_to_outlook(email_address)
