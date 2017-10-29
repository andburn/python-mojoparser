"""Test the mojoshader parse() parse failure"""
import pytest
import os
from mojoparser import *


def read_data(file, mode="rb"):
	with open(os.path.join("tests", "data", file), mode) as f:
		return f.read()


def test_parse_failure_error_message():
	"""Test the error representation"""
	with pytest.raises(ParseFailureError) as err:
		Parser().parse(read_data("corrupt.bin"))

	error = err.value
	assert str(error) == "MojoShader Parse Failure (7)"


def test_parse_failure_error_properties():
	"""Test the error properties"""
	with pytest.raises(ParseFailureError) as err:
		Parser().parse(read_data("corrupt.bin"))

	error = err.value
	assert error.count == 7

	assert "Shader has corrupt CTAB data" == error.errors[0]
	for i in range(1, error.count):
		assert "unknown token" in error.errors[i]
