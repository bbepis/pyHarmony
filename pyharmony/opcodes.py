"""
Contains constant values for opcode names, to allow for easier instruction creation.
"""

POP_TOP = "POP_TOP"
ROT_TWO = "ROT_TWO"
ROT_THREE = "ROT_THREE"
DUP_TOP = "DUP_TOP"
DUP_TOP_TWO = "DUP_TOP_TWO"
ROT_FOUR = "ROT_FOUR"
NOP = "NOP"
UNARY_POSITIVE = "UNARY_POSITIVE"
UNARY_NEGATIVE = "UNARY_NEGATIVE"
UNARY_NOT = "UNARY_NOT"
UNARY_INVERT = "UNARY_INVERT"
BINARY_MATRIX_MULTIPLY = "BINARY_MATRIX_MULTIPLY"
INPLACE_MATRIX_MULTIPLY = "INPLACE_MATRIX_MULTIPLY"
BINARY_POWER = "BINARY_POWER"
BINARY_MULTIPLY = "BINARY_MULTIPLY"
BINARY_MODULO = "BINARY_MODULO"
BINARY_ADD = "BINARY_ADD"
BINARY_SUBTRACT = "BINARY_SUBTRACT"
BINARY_SUBSCR = "BINARY_SUBSCR"
BINARY_FLOOR_DIVIDE = "BINARY_FLOOR_DIVIDE"
BINARY_TRUE_DIVIDE = "BINARY_TRUE_DIVIDE"
INPLACE_FLOOR_DIVIDE = "INPLACE_FLOOR_DIVIDE"
INPLACE_TRUE_DIVIDE = "INPLACE_TRUE_DIVIDE"
GET_AITER = "GET_AITER"
GET_ANEXT = "GET_ANEXT"
BEFORE_ASYNC_WITH = "BEFORE_ASYNC_WITH"
BEGIN_FINALLY = "BEGIN_FINALLY"
END_ASYNC_FOR = "END_ASYNC_FOR"
INPLACE_ADD = "INPLACE_ADD"
INPLACE_SUBTRACT = "INPLACE_SUBTRACT"
INPLACE_MULTIPLY = "INPLACE_MULTIPLY"
INPLACE_MODULO = "INPLACE_MODULO"
STORE_SUBSCR = "STORE_SUBSCR"
DELETE_SUBSCR = "DELETE_SUBSCR"
BINARY_LSHIFT = "BINARY_LSHIFT"
BINARY_RSHIFT = "BINARY_RSHIFT"
BINARY_AND = "BINARY_AND"
BINARY_XOR = "BINARY_XOR"
BINARY_OR = "BINARY_OR"
INPLACE_POWER = "INPLACE_POWER"
GET_ITER = "GET_ITER"
GET_YIELD_FROM_ITER = "GET_YIELD_FROM_ITER"
PRINT_EXPR = "PRINT_EXPR"
LOAD_BUILD_CLASS = "LOAD_BUILD_CLASS"
YIELD_FROM = "YIELD_FROM"
GET_AWAITABLE = "GET_AWAITABLE"
INPLACE_LSHIFT = "INPLACE_LSHIFT"
INPLACE_RSHIFT = "INPLACE_RSHIFT"
INPLACE_AND = "INPLACE_AND"
INPLACE_XOR = "INPLACE_XOR"
INPLACE_OR = "INPLACE_OR"
WITH_CLEANUP_START = "WITH_CLEANUP_START"
WITH_CLEANUP_FINISH = "WITH_CLEANUP_FINISH"
RETURN_VALUE = "RETURN_VALUE"
IMPORT_STAR = "IMPORT_STAR"
SETUP_ANNOTATIONS = "SETUP_ANNOTATIONS"
YIELD_VALUE = "YIELD_VALUE"
POP_BLOCK = "POP_BLOCK"
END_FINALLY = "END_FINALLY"
POP_EXCEPT = "POP_EXCEPT"
STORE_NAME = "STORE_NAME"
DELETE_NAME = "DELETE_NAME"
UNPACK_SEQUENCE = "UNPACK_SEQUENCE"
FOR_ITER = "FOR_ITER"
UNPACK_EX = "UNPACK_EX"
STORE_ATTR = "STORE_ATTR"
DELETE_ATTR = "DELETE_ATTR"
STORE_GLOBAL = "STORE_GLOBAL"
DELETE_GLOBAL = "DELETE_GLOBAL"
LOAD_CONST = "LOAD_CONST"
LOAD_NAME = "LOAD_NAME"
BUILD_TUPLE = "BUILD_TUPLE"
BUILD_LIST = "BUILD_LIST"
BUILD_SET = "BUILD_SET"
BUILD_MAP = "BUILD_MAP"
LOAD_ATTR = "LOAD_ATTR"
COMPARE_OP = "COMPARE_OP"
IMPORT_NAME = "IMPORT_NAME"
IMPORT_FROM = "IMPORT_FROM"
JUMP_FORWARD = "JUMP_FORWARD"
JUMP_IF_FALSE_OR_POP = "JUMP_IF_FALSE_OR_POP"
JUMP_IF_TRUE_OR_POP = "JUMP_IF_TRUE_OR_POP"
JUMP_ABSOLUTE = "JUMP_ABSOLUTE"
POP_JUMP_IF_FALSE = "POP_JUMP_IF_FALSE"
POP_JUMP_IF_TRUE = "POP_JUMP_IF_TRUE"
LOAD_GLOBAL = "LOAD_GLOBAL"
SETUP_FINALLY = "SETUP_FINALLY"
LOAD_FAST = "LOAD_FAST"
STORE_FAST = "STORE_FAST"
DELETE_FAST = "DELETE_FAST"
RAISE_VARARGS = "RAISE_VARARGS"
CALL_FUNCTION = "CALL_FUNCTION"
MAKE_FUNCTION = "MAKE_FUNCTION"
BUILD_SLICE = "BUILD_SLICE"
LOAD_CLOSURE = "LOAD_CLOSURE"
LOAD_DEREF = "LOAD_DEREF"
STORE_DEREF = "STORE_DEREF"
DELETE_DEREF = "DELETE_DEREF"
CALL_FUNCTION_KW = "CALL_FUNCTION_KW"
CALL_FUNCTION_EX = "CALL_FUNCTION_EX"
SETUP_WITH = "SETUP_WITH"
LIST_APPEND = "LIST_APPEND"
SET_ADD = "SET_ADD"
MAP_ADD = "MAP_ADD"
LOAD_CLASSDEREF = "LOAD_CLASSDEREF"
EXTENDED_ARG = "EXTENDED_ARG"
BUILD_LIST_UNPACK = "BUILD_LIST_UNPACK"
BUILD_MAP_UNPACK = "BUILD_MAP_UNPACK"
BUILD_MAP_UNPACK_WITH_CALL = "BUILD_MAP_UNPACK_WITH_CALL"
BUILD_TUPLE_UNPACK = "BUILD_TUPLE_UNPACK"
BUILD_SET_UNPACK = "BUILD_SET_UNPACK"
SETUP_ASYNC_WITH = "SETUP_ASYNC_WITH"
FORMAT_VALUE = "FORMAT_VALUE"
BUILD_CONST_KEY_MAP = "BUILD_CONST_KEY_MAP"
BUILD_STRING = "BUILD_STRING"
BUILD_TUPLE_UNPACK_WITH_CALL = "BUILD_TUPLE_UNPACK_WITH_CALL"
LOAD_METHOD = "LOAD_METHOD"
CALL_METHOD = "CALL_METHOD"
CALL_FINALLY = "CALL_FINALLY"
POP_FINALLY = "POP_FINALLY"
