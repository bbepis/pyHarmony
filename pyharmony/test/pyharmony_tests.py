import unittest
import sys
import types
from bytecode import Bytecode, Instr
from pyharmony import Patch, PatchHandler, transpiler, prefix, postfix, opcodes


def test_function(arg1, arg2):
    arg2.run = True
    return arg1 + 10


thismodule = sys.modules[__name__]


class pyHarmonyTests(unittest.TestCase):
    def setUp(self):
        self.patch_handler = PatchHandler("unit_test")

    def tearDown(self) -> None:
        self.patch_handler.destroy()

    @staticmethod
    def getArg2():
        arg2 = types.SimpleNamespace()
        arg2.run = False
        return arg2



    # Can't use decorators in tests because they all apply at once

    def test_transpiler(self):
        def my_transpiler(bytecode: Bytecode) -> Bytecode:
            bytecode[4] = Instr(opcodes.LOAD_CONST, 20)
            return bytecode

        transpiler(thismodule, "test_function", handler=self.patch_handler)(my_transpiler)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 120)
        self.assertTrue(arg2.run)



    def test_prefix_run_none(self):
        def my_prefix(arg_obj: dict) -> None:
            arg_obj["arg1"] += 1

        prefix(thismodule, "test_function", handler=self.patch_handler)(my_prefix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 111)
        self.assertTrue(arg2.run)



    def test_prefix_run_true(self):
        def my_prefix(arg_obj: dict) -> bool:
            arg_obj["arg1"] += 1
            return True

        prefix(thismodule, "test_function", handler=self.patch_handler)(my_prefix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 111)
        self.assertTrue(arg2.run)



    def test_prefix_run_false(self):
        def my_prefix(arg_obj: dict) -> bool:
            arg_obj["arg1"] += 1
            return False

        prefix(thismodule, "test_function", handler=self.patch_handler)(my_prefix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertIsNone(test_function(100, arg2))
        self.assertFalse(arg2.run)



    def test_postfix(self):
        def my_postfix(arg_obj: dict) -> None:
            arg_obj["__result"] = 20

        postfix(thismodule, "test_function", handler=self.patch_handler)(my_postfix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 20)
        self.assertTrue(arg2.run)



    def test_prefix_true_postfix(self):
        def my_prefix(arg_obj: dict) -> bool:
            arg_obj["arg1"] += 1
            return True

        def my_postfix(arg_obj: dict) -> None:
            arg_obj["__result"] += 20

        prefix(thismodule, "test_function", handler=self.patch_handler)(my_prefix)
        postfix(thismodule, "test_function", handler=self.patch_handler)(my_postfix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 131)
        self.assertTrue(arg2.run)



    def test_prefix_false_postfix(self):
        def my_prefix(arg_obj: dict) -> bool:
            return False

        def my_postfix(arg_obj: dict) -> None:
            arg_obj["arg2"].postfix_run = True

        prefix(thismodule, "test_function", handler=self.patch_handler)(my_prefix)
        postfix(thismodule, "test_function", handler=self.patch_handler)(my_postfix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), None)
        self.assertFalse(arg2.run)
        self.assertTrue(arg2.postfix_run)



    def test_patch_disabled(self):

        def my_postfix(arg_obj: dict) -> None:
            arg_obj["__result"] = 1234

        postfix(thismodule, "test_function", handler=self.patch_handler, enabled=False)(my_postfix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 110)
        self.assertTrue(arg2.run)



    def test_patch_apply_false(self):

        def my_postfix(arg_obj: dict) -> None:
            arg_obj["__result"] = 1234

        postfix(thismodule, "test_function", handler=self.patch_handler, apply=False)(my_postfix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 110)
        self.assertTrue(arg2.run)

        self.patch_handler.patch_all()

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 1234)
        self.assertTrue(arg2.run)



    def test_unpatch_all(self):

        def my_postfix(arg_obj: dict) -> None:
            arg_obj["__result"] = 1234

        postfix(thismodule, "test_function", handler=self.patch_handler)(my_postfix)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 1234)
        self.assertTrue(arg2.run)

        self.patch_handler.unpatch_all()

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 110)
        self.assertTrue(arg2.run)



    def test_patch_count(self):

        self.assertEqual(len(self.patch_handler.patches), 0)

        def my_postfix(arg_obj: dict) -> None:
            arg_obj["__result"] = 1234

        postfix(thismodule, "test_function", handler=self.patch_handler)(my_postfix)

        self.assertEqual(len(self.patch_handler.patches), 1)



    def test_add_patch_manually(self):

        def my_postfix(arg_obj: dict) -> None:
            arg_obj["__result"] = 1234

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 110)
        self.assertTrue(arg2.run)

        patch = Patch(thismodule, "test_function", postfix_func=my_postfix)
        self.patch_handler.patches.append(patch)

        self.patch_handler.patch_all()

        arg2 = pyHarmonyTests.getArg2()
        
        self.assertEqual(test_function(100, arg2), 1234)
        self.assertTrue(arg2.run)



    def test_patch_priority_hinting(self):

        def my_postfix_1(arg_obj: dict) -> None:
            arg_obj["__result"] = 1

        def my_postfix_2(arg_obj: dict) -> None:
            arg_obj["__result"] = 2

        # my_postfix_2 should run last here, overwriting the result
        postfix(thismodule, "test_function", handler=self.patch_handler, priority_hint=1)(my_postfix_1)
        postfix(thismodule, "test_function", handler=self.patch_handler, priority_hint=-1)(my_postfix_2)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 2)

        # do it in reverse to ensure it's not a fluke
        self.patch_handler.patches.clear()

        postfix(thismodule, "test_function", handler=self.patch_handler, priority_hint=-1)(my_postfix_1)
        postfix(thismodule, "test_function", handler=self.patch_handler, priority_hint=1)(my_postfix_2)

        arg2 = pyHarmonyTests.getArg2()

        self.assertEqual(test_function(100, arg2), 1)


if __name__ == "__main__":
    unittest.main()
