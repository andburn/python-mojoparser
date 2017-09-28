import sys
from pyparsing import (
	Word, Literal, OneOrMore, ZeroOrMore, Suppress, Optional, alphas, nums, alphanums
)

keywords = """
attribute const uniform varying centroid break continue do for while if else in
out inout float int void bool true false invariant discard return mat2 mat3 mat4
mat2x2 mat2x3 mat2x4 mat3x2 mat3x3 mat3x4 mat4x2 mat4x3 mat4x4 vec2 vec3 vec4
ivec2 ivec3 ivec4 bvec2 bvec3 bvec4 sampler1D sampler2D sampler3D samplerCube
sampler1DShadow sampler2DShadow struct
"""
reserved = """
asm class union enum typedef template this packed goto switch default inline
noinline volatile public static extern external interface long short double half
fixed unsigned lowp mediump highp precision input output hvec2 hvec3 hvec4 dvec2
dvec3 dvec4 fvec2 fvec3 fvec4 sampler2DRect sampler3DRect sampler2DRectShadow
sizeof cast namespace using
"""

LBRACE, RBRACE, LBRACK, RBRACK, LPAR, RPAR, LANG, RANG = map(Suppress, "{}[]()<>")
PLUS, DASH, SLASH, ASTERIX, PERCENT, EQ = map(Literal, "+-/*%=")
CARET, BAR, AMPERSAND, TILDE, BANG, COLON, SEMI, COMMA, HASH = map(Suppress, "^|&~!:;,#")

ident = Word(alphas, alphanums + "_") # gl_* are reserved, but doesn't really matter


def main():
	sample = """
	#version 101
	precision mediump float;

	#define PI 3.141519

	uniform float time;
	uniform vec2 mouse;
	uniform vec2 resolution;

	void main( void ) {

		vec2 st = (gl_FragCoord.xy * 2.0 - resolution) / resolution.y;
		vec2 m;
		m.x = (mouse.x * 2.0 - 1.0) * PI;
		m.y = mouse.y * 5.0;

		vec3 origin = vec3(2.5 * sin(m.x), 0.5 + m.y, 2.5 * cos(m.x));
		vec3 target = vec3(0.0, 0.5, 0.0);
		vec3 cz = normalize(target - origin);
		vec3 cx = cross(cz, vec3(0.0, 1.0, 0.0));
		vec3 cy = cross(cx, cz);
		vec3 direction = normalize(cx * st.x + cy * st.y + cz * 1.0);

		vec3 color = render(origin, direction);

		gl_FragColor = vec4(color, 1.0);
	}
	"""

	version = Suppress("#version") + Word(nums)

	name = Word(alphanums + "_")
	swizzle = Literal(".") + Word("xyzw", min=1, max=4)
	ident = name + Optional(swizzle)

	variable = Word(alphanums) + name + Suppress(";")
	uniform = Literal("uniform") + variable
	index = Literal("[") + Word(nums) + Literal("]")
	define = Suppress("#define") + name + Word(alphanums + "_") + Optional(index)

	main = Literal("void main()") + Literal("{")
	params = ZeroOrMore(ident + Optional(","))
	call = Literal("texture2D") + "(" + params + ")" + ";"

	operator = Word("+-\*", exact=1)
	operation = ident + "=" + ident + operator + ident
	statement = ident + "=" + call | operation + ";"

	rule = version + OneOrMore(variable) + OneOrMore(uniform) \
		+ OneOrMore(define) + main + OneOrMore(statement)

	print(rule.parseString(sample))


if __name__ == "__main__":
	main()
