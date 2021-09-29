import sys

if (__package__ is None or __package__ == ""):
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))
    __package__ = "pyharmony"

from .pyharmony import transpiler, prefix, postfix
from . import opcodes

import dis
import opcode

#from . import opcode as Opcode
from bytecode import Instr, Bytecode

# codeObj = testFunction.__code__

# print(disassembly)
# print(list(testFunction.__code__.co_code))
# print(id(testFunction))

# inst = disassembly[2]

# disassembly[2] = dis.Instruction('BINARY_SUBTRACT', opcode.opmap['BINARY_SUBTRACT'], inst.arg, None, None, None, None, None)

# new_bytecode = create_bytecode(disassembly)
# print(list(new_bytecode))
# new_co = create_code_object(testFunction.__code__, new_bytecode)
# testFunction.__code__ = new_co

thismodule = sys.modules[__name__]

#dis.dis(testfunc2)
#testfunc3(1)


def test_function(a):
    return a + 10

print(test_function(100))



@transpiler(thismodule, "test_function")
def my_transpiler(bytecode: Bytecode) -> Bytecode:
    bytecode[1] = Instr(opcodes.LOAD_CONST, 20)
    return bytecode

print(test_function(100))



@prefix(thismodule, "test_function")
def my_prefix(arg_obj: dict) -> bool:
    arg_obj["a"] += 1
    return True

print(test_function(100))



@postfix(thismodule, "test_function")
def my_postfix(arg_obj: dict) -> None:
    arg_obj["__result"] = 6
    return

print(test_function(100))



@prefix(thismodule, "test_function")
def my_prefix_2(arg_obj: dict) -> bool:
    return False

print(test_function(100))

#dis.dis(test_function)


def new_value():
    return 0
    #bytecode.insert(2, Instr(CALL_FUNCTION, 0))
# bytecode[2] = Instr(BINARY_MODULO)


#list(map(lambda key: print('    %s = Opcode(\'%s\', %s)' % (key, key, opcode.opmap[key])), opcode.opmap))
#list(map(lambda key: print('%s = \"%s\"' % (key, key)), opcode.opmap))

#bytecode[1] = Instr("LOAD_DEREF", FreeVar('testFunc4'))
#bytecode.freevars["testFunc4"] = testFunc4

# co = testFunction.__code__
# testFunction.__code__ = types.CodeType(co.co_argcount, co.co_kwonlyargcount,
#              co.co_nlocals, co.co_stacksize, co.co_flags,
#              co.co_code, co.co_consts, co.co_names,
#              co.co_varnames, co.co_filename,
#              co.co_name,
#              co.co_firstlineno, co.co_lnotab, co.co_freevars,
#              co.co_cellvars)


def kwtest(a, b):

    def inner(*args, **kwargs):
        return

    kwargs = {} # "a": 1, "b": 2
    kwargs["a"] = a
    kwargs["b"] = b

    a = kwargs["a"]
    b = kwargs["b"]

    if not a:
        return

    inner(None, **kwargs)

# dis.dis(kwtest)

# for instr in Bytecode.from_code(kwtest.__code__):
#     print(instr)

#def none_func():
#    return

#print(none_func())