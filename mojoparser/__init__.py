from .parser import Parser
from .mojoshader import *


class LibraryNotFoundException(OSError):
	pass


class ParseFailureError(Exception):
	pass


class ProfileNotSupportedError(Exception):
	pass
