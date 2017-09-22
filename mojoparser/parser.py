import os
import ctypes
import ctypes.util
from enum import Enum
from .mojoshader import *


def load_lib(*names):
	for name in names:
		libname = ctypes.util.find_library(name)
		if libname:
			return ctypes.CDLL(libname)
		else:
			dll_path = os.path.join(os.getcwd(), "%s.dll" % (name))
			return ctypes.CDLL(dll_path)
	raise LibraryNotFoundException("Could not load the library %r" % (names[0]))


class Profile(Enum):
	GLSL110 = "glsl"
	GLSL120 = "glsl120"


class Parser:
	def __init__(self):
		self.lib = load_lib("mojoshader")
		self.mojo_parse = self.define_method()

	def define_method(self):
		self.lib.MOJOSHADER_parse.argtypes = [
			ctypes.c_char_p,
			ctypes.c_char_p,
			ctypes.POINTER(ctypes.c_char),
			ctypes.c_int,
			ctypes.POINTER(Swizzle),
			ctypes.c_int,
			ctypes.POINTER(SamplerMap),
			ctypes.c_int,
			ctypes.c_void_p, # MOJOSHADER_malloc
			ctypes.c_void_p, # MOJOSHADER_free
			ctypes.c_void_p
		]
		self.lib.MOJOSHADER_parse.restype = ctypes.POINTER(ParseData)
		return self.lib.MOJOSHADER_parse

	def parse(self, data, profile=Profile.GLSL110):
		if profile != Profile.GLSL110 and profile != Profile.GLSL120:
			raise ProfileNotSupportedError("{} is not a supported profile".format(profile))
		parse_data = self.mojo_parse(
				profile.value.encode("ascii"), b'main', data, len(data),
				None, 0, None, 0, None, None, None).contents
		if parse_data.error_count > 0:
			# TODO show all errors, not just first
			raise ParseFailureError("MojoShader parse failed: {}".format(
					parse_data.errors[0].error))
		return parse_data
