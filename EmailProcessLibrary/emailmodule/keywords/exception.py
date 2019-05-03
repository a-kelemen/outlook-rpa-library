from __future__ import absolute_import, division, generators, print_function, unicode_literals


class EmailLibraryException(Exception):
	pass
	#ROBOT_SUPPRESS_NAME = True


class OutlookException(EmailLibraryException):
	pass


class DirectoryNotFoundException(EmailLibraryException):
	pass


class FileNotFoundException(EmailLibraryException):
	pass


class EmailNotFoundException(EmailLibraryException):
	pass