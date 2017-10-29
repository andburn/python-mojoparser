"""Test the mojoshader parse() ctype setup"""
import pytest
import io
import os
from mojoparser import *


def read_data(file, mode="rb"):
	with open(os.path.join("tests", "data", file), mode) as f:
		return f.read()


@pytest.fixture
def parse_data():
	p = Parser()
	return p.parse(read_data("shader.bin"), Profile.GLSL120)


def test_error_count(parse_data):
	assert parse_data.error_count == 0


def test_profile(parse_data):
	assert parse_data.profile == b"glsl"


def test_instruction_count(parse_data):
	assert parse_data.instruction_count == 10


def test_shader_version(parse_data):
	assert parse_data.major_ver == 2
	assert parse_data.minor_ver == 0


def test_shader_type(parse_data):
	assert parse_data.shader_type == ShaderType.VERTEX


def test_uniform_count(parse_data):
	assert parse_data.uniform_count == 8


def test_uniform_values(parse_data):
	for i in range(parse_data.uniform_count):
		assert parse_data.uniforms[i].name == b"vs_c" + bytes(str(i), "ascii")
		assert parse_data.uniforms[i].type == UniformType.FLOAT
		assert parse_data.uniforms[i].index == i
		assert parse_data.uniforms[i].array_count == 0
		assert parse_data.uniforms[i].constant == 0


def test_constant_count(parse_data):
	assert parse_data.constant_count == 1


def test_constant_values(parse_data):
	assert parse_data.constants[0].type == UniformType.FLOAT
	assert parse_data.constants[0].index == 8
	assert list(parse_data.constants[0].value.f) == [2.0, 0.0, 0.0, 0.0]


def test_sampler_count(parse_data):
	assert parse_data.sampler_count == 0


def test_attribute_count(parse_data):
	assert parse_data.attribute_count == 3


def test_attribute_values(parse_data):
	for i in range(parse_data.attribute_count):
		assert parse_data.attributes[i].name == b"vs_v" + bytes(str(i), "ascii")
		assert parse_data.attributes[i].index == 0
		assert parse_data.attributes[i].usage == i * 5


def test_output_count(parse_data):
	assert parse_data.output_count == 3


def test_attribute_values(parse_data):
	assert parse_data.outputs[0].name == b"vs_oPos"
	assert parse_data.outputs[1].name == b"vs_oD0"
	assert parse_data.outputs[2].name == b"vs_oT0"


def test_swizzle_count(parse_data):
	assert parse_data.swizzle_count == 0


def test_symbol_count(parse_data):
	assert parse_data.symbol_count == 5


def test_symbol_names(parse_data):
	assert parse_data.symbols[0].name == b"_LightColor0"
	assert parse_data.symbols[1].name == b"_LightingBlend"
	assert parse_data.symbols[2].name == b"_MainTex_ST"
	assert parse_data.symbols[3].name == b"glstate_lightmodel_ambient"
	assert parse_data.symbols[4].name == b"glstate_matrix_mvp"


def test_symbol_indicies(parse_data):
	assert parse_data.symbols[0].register_index == 5
	assert parse_data.symbols[1].register_index == 6
	assert parse_data.symbols[2].register_index == 7
	assert parse_data.symbols[3].register_index == 4
	assert parse_data.symbols[4].register_index == 0


def test_symbol_counts(parse_data):
	assert parse_data.symbols[0].register_count == 1
	assert parse_data.symbols[1].register_count == 1
	assert parse_data.symbols[2].register_count == 1
	assert parse_data.symbols[3].register_count == 1
	assert parse_data.symbols[4].register_count == 4


def test_symbol_regset(parse_data):
	for i in range(parse_data.symbol_count):
		assert parse_data.symbols[i].register_set == SymbolRegisterSet.FLOAT4


def test_first_symbol_info(parse_data):
	assert parse_data.symbols[0].info.parameter_class == SymbolClass.VECTOR
	assert parse_data.symbols[0].info.parameter_type == SymbolType.FLOAT
	assert parse_data.symbols[0].info.rows == 1
	assert parse_data.symbols[0].info.columns == 4
	assert parse_data.symbols[0].info.elements == 1
	assert parse_data.symbols[0].info.member_count == 0


def test_last_symbol_info(parse_data):
	assert parse_data.symbols[4].info.parameter_class == SymbolClass.MATRIX_ROWS
	assert parse_data.symbols[4].info.parameter_type == SymbolType.FLOAT
	assert parse_data.symbols[4].info.rows == 4
	assert parse_data.symbols[4].info.columns == 4
	assert parse_data.symbols[4].info.elements == 1
	assert parse_data.symbols[4].info.member_count == 0
