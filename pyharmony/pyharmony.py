"""
Contains the main functionality, classes and decorators for pyHarmony.
"""

from collections import namedtuple
import types
from typing import Callable, List, Dict, Optional, Tuple
from bytecode import Bytecode, Instr, Label
from . import opcodes


# Type hinting declarations

FunctionTarget = Tuple[object, str]
FunctionDefinition = Tuple[types.FunctionType, types.CodeType]

PatchTarget = namedtuple("PatchTarget", ["target_object", "target_function_name"])

def _assemble_prefix(bytecode: Bytecode, prefix_func: types.FunctionType) -> None:
    """
    Inserts the required bytecode for prefix functionality.
    """

    instruction_set = []

    # Create an empty dictionary and put it in a variable named "_pyharmony_prefix_state"

    state_variable = "_pyharmony_prefix_state"
    instruction_set.append(Instr(opcodes.BUILD_MAP, 0))
    instruction_set.append(Instr(opcodes.STORE_FAST, state_variable))

    for arg_name in bytecode.argnames:
        # Insert each argument into the dictionary
        instruction_set.append(Instr(opcodes.LOAD_FAST, arg_name))
        instruction_set.append(Instr(opcodes.LOAD_FAST, state_variable))
        instruction_set.append(Instr(opcodes.LOAD_CONST, arg_name))
        instruction_set.append(Instr(opcodes.STORE_SUBSCR))

    # Call our higher-level prefix code
    instruction_set.append(Instr(opcodes.LOAD_CONST, prefix_func))
    instruction_set.append(Instr(opcodes.LOAD_FAST, state_variable))
    instruction_set.append(Instr(opcodes.CALL_FUNCTION, 1))

    # Check if the prefix returned true or false
    continue_label = Label()

    instruction_set.append(Instr(opcodes.POP_JUMP_IF_TRUE, continue_label))

    # Exit if false
    instruction_set.append(Instr(opcodes.LOAD_CONST, None))
    instruction_set.append(Instr(opcodes.RETURN_VALUE))

    # Otherwise continue, and set parameters to the potentially modified values of the dictionary

    instruction_set.append(continue_label)

    for arg_name in bytecode.argnames:
        # Insert each argument into the dictionary
        instruction_set.append(Instr(opcodes.LOAD_FAST, state_variable))
        instruction_set.append(Instr(opcodes.LOAD_CONST, arg_name))
        instruction_set.append(Instr(opcodes.BINARY_SUBSCR))
        instruction_set.append(Instr(opcodes.STORE_FAST, arg_name))

    # Done with assembling, main execution begins here

    # Insert instructions to the start of the function

    for instruction in reversed(instruction_set):
        bytecode.insert(0, instruction)


def _assemble_postfix(bytecode: Bytecode, postfix_func: types.FunctionType) -> None:
    """
    Inserts the required bytecode for postfix functionality.
    """

    instruction_set = []

    # Get a list of variable names. This will be a bit awkward, as we compile to a concrete bytecode implementation
    concrete_bytecode = bytecode.to_concrete_bytecode()

    # Create a label for instructions to jump to, instead of returning immediately

    postfix_label = Label()
    instruction_set.append(postfix_label)

    # Create an empty dictionary and put it in a variable named "_pyharmony_postfix_state"

    state_variable = "_pyharmony_postfix_state"
    instruction_set.append(Instr(opcodes.BUILD_MAP, 0))
    instruction_set.append(Instr(opcodes.STORE_FAST, state_variable))

    for arg_name in bytecode.argnames:
        # Insert each argument into the dictionary
        instruction_set.append(Instr(opcodes.LOAD_FAST, arg_name))
        instruction_set.append(Instr(opcodes.LOAD_FAST, state_variable))
        instruction_set.append(Instr(opcodes.LOAD_CONST, arg_name))
        instruction_set.append(Instr(opcodes.STORE_SUBSCR))

    for arg_name in concrete_bytecode.varnames:
        # Insert each variable into the dictionary
        instruction_set.append(Instr(opcodes.LOAD_FAST, arg_name))
        instruction_set.append(Instr(opcodes.LOAD_FAST, state_variable))
        instruction_set.append(Instr(opcodes.LOAD_CONST, arg_name))
        instruction_set.append(Instr(opcodes.STORE_SUBSCR))

    # Insert the result into the dictionary, which has been lingering on the stack this entire time
    # This will replace any variable named "__result" but that's very unlikely

    instruction_set.append(Instr(opcodes.LOAD_FAST, state_variable))
    instruction_set.append(Instr(opcodes.LOAD_CONST, "__result"))
    instruction_set.append(Instr(opcodes.STORE_SUBSCR))

    # Call our higher-level postfix code

    instruction_set.append(Instr(opcodes.LOAD_CONST, postfix_func))
    instruction_set.append(Instr(opcodes.LOAD_FAST, state_variable))
    instruction_set.append(Instr(opcodes.CALL_FUNCTION, 1))

    # Get our return value

    instruction_set.append(Instr(opcodes.LOAD_FAST, state_variable))
    instruction_set.append(Instr(opcodes.LOAD_CONST, "__result"))
    instruction_set.append(Instr(opcodes.BINARY_SUBSCR))

    # Return it

    instruction_set.append(Instr(opcodes.RETURN_VALUE))

    # Done with assembling, execution ends here

    # Replace all instances of RETURN_VALUE (including the prefix) to jump to our new bytecode

    for index, instruction in enumerate(bytecode):
        if isinstance(instruction, Instr) and instruction.name == opcodes.RETURN_VALUE:
            bytecode[index] = Instr(opcodes.JUMP_ABSOLUTE, postfix_label)

    # Insert everything at the very end

    bytecode.extend(instruction_set)


def _reevaluate_function(target_object: object, target_function_name: str) -> None:
    """
    Recalculates the code object for a function, including the defined function hooks.
    """

    if not hasattr(target_object, target_function_name):
        # Do nothing if the target function doesn't exist.
        return

    func_def: types.FunctionType
    func_def_code: types.CodeType

    if (target_object, target_function_name) not in original_function_definitions:

        # We don't have an original version of the function. Get it
        func_def = getattr(target_object, target_function_name)

        if not isinstance(func_def, types.FunctionType):
            # This isn't a function.
            # Arguably, we can move this check into the decorators
            return

        func_def_code = func_def.__code__

        original_function_definitions[(target_object, target_function_name)] = (func_def, func_def.__code__)
    else:
        # Use our stored function / code definition
        func_def, func_def_code = original_function_definitions[(target_object, target_function_name)]

    # Convert to bytecode we can work with
    func_working_bytecode = Bytecode.from_code(func_def_code)

    # Figure out what we actually have for patching

    patch_target = PatchTarget(target_object, target_function_name)

    all_patches = [p for plist in (h.patches for name, h in all_patch_handlers.items()) for p in plist if p.enabled and p.target == patch_target]

    def filter_and_sort(predicate: types.LambdaType) -> List[Patch]:
        return sorted(
            [p for p in all_patches if predicate(p) is not None],
            key=lambda x: x.priority_hint or 0, reverse=True)

    our_transpilers: List[Patch] = filter_and_sort(lambda p: p.transpiler_func)
    our_prefixes: List[Patch] = filter_and_sort(lambda p: p.prefix_func)
    our_postfixes: List[Patch] = filter_and_sort(lambda p: p.postfix_func)

    # Perform transpilers first.
    # Transpilers expect the original instruction set, so things like prefixes and postfixes
    #   (which require manual instruction insertions) have to happen after

    for patch in our_transpilers:
        func_working_bytecode = patch.transpiler_func(func_working_bytecode)

    # Do prefixes.
    # We do half the work in bytecode and the other half in regular code, just to make it easier
    #   instead of writing everything in bytecode

    def do_prefixes(arg_object: dict) -> bool:
        for patch in our_prefixes:
            return_val = patch.prefix_func(arg_object)

            if return_val is not None and not return_val:
                return False

        return True

    if len(our_prefixes) > 0:    # Don't bother with it if there's no prefixes
        _assemble_prefix(func_working_bytecode, do_prefixes)

    # Do postfixes.

    def do_postfixes(arg_object: dict) -> bool:
        for patch in our_postfixes:
            patch.postfix_func(arg_object)

    if len(our_postfixes) > 0:    # Don't bother with it if there's no postfixes
        _assemble_postfix(func_working_bytecode, do_postfixes)

    # Set the original function to use our bytecode

    func_def.__code__ = func_working_bytecode.to_code()



# Patch classes

class Patch:
    """
    A patch definition, for use by PatchHandler.
    """
    def __init__(self,
                 target_object: object,
                 target_function_name: str,
                 patch_name: Optional[str] = None,
                 *,
                 enabled: bool = True,
                 priority_hint: int = 0,
                 transpiler_func: Callable[[Bytecode], Bytecode] = None,
                 prefix_func: Callable[[object], Optional[bool]] = None,
                 postfix_func: Callable[[object], None] = None) -> None:
        """
        Creates a patch object. Only supply a single transpiler, prefix or postfix function.

        target_object: The object that the target function belongs to.
        target_function_name: The attribute name of the function to patch, which belongs to target_object.
        patch_name: The name of this specific patch. Used for logging
        enabled: Whether or not this patch is enabled. If false, then this patch will be skipped over when evaluating which patches to apply to the target method.
        priority_hint: An integer hint used by the patch library to determine the order patches should be applied in. Larger numbers have higher priority, while smaller (including negative) numbers have lower priority. Defaults to zero
        """

        self.target = PatchTarget(target_object, target_function_name)

        function_count = sum(1 for f in [transpiler_func, prefix_func, postfix_func] if f is not None)

        if function_count != 1:
            raise ValueError(f"Expected a single patch function to be supplied, instead recieved {function_count}")

        remaining_function = transpiler_func or prefix_func or postfix_func

        self.patch_name = patch_name or remaining_function.__name__

        self.priority_hint = priority_hint
        self.enabled = enabled

        self.transpiler_func = transpiler_func
        self.prefix_func = prefix_func
        self.postfix_func = postfix_func


class PatchHandler:
    """
    A class containing a collection of patches, and methods to facilitate applying them.
    """
    def __init__(self, instance_name: Optional[str] = None):
        """
        Creates a new PatchHandler, or if a previous one with the same instance_name already exists, retrieves the patches from that instance instead.

        If instance_name is not provided, uses id() to generate an instance name.
        """

        self.instance_name = instance_name or str(id(self))
        self.patches: List[Patch]

        existing_instance = all_patch_handlers.get(self.instance_name, None)

        if existing_instance is not None:
            self.patches = existing_instance.patches
        else:
            self.patches = []
            all_patch_handlers[self.instance_name] = self

    def patch_all(self):
        """
        (Re)applies all patches that belong to this handler, respecting the Patch.enabled property.
        """

        targets = set(p.target for p in self.patches) # if p.enabled

        for target in targets:
            _reevaluate_function(target.target_object, target.target_function_name)

    def unpatch_all(self):
        """
        Sets all patches to disabled, and reapplies them resulting in all patches being removed.
        """

        for patch in self.patches:
            patch.enabled = False

        self.patch_all()

    def destroy(self):
        """
        Removes this handler (and instance_name) from global PatchHandler state tracking. Results in all patches provided by this handler being unpatched.

        Please use this if you are creating a lot of handlers and discarding them, to keep the global state tracker performant.
        """

        if self.instance_name in all_patch_handlers:
            all_patch_handlers.pop(self.instance_name)

        self.unpatch_all()



# Global state

original_function_definitions: Dict[FunctionTarget, FunctionDefinition] = {}

all_patch_handlers: Dict[str, PatchHandler] = {}
anonymous_handler: PatchHandler = PatchHandler("_anonymous")



# Decorators

def __create_decorator_patch(target: PatchTarget,
                             patch_name: Optional[str],
                             priority_hint: Optional[int],
                             handler: Optional[PatchHandler],
                             enabled: bool,
                             apply: bool,
                             *,
                             transpiler_func=None,
                             prefix_func=None,
                             postfix_func=None):

    patch = Patch(target.target_object,
                  target.target_function_name,
                  patch_name,
                  enabled=enabled,
                  priority_hint=priority_hint,
                  transpiler_func=transpiler_func,
                  prefix_func=prefix_func,
                  postfix_func=postfix_func)

    handler = handler or anonymous_handler
    handler.patches.append(patch)

    if apply:
        handler.patch_all()


def transpiler(target_object: object,
               target_function_name: str,
               patch_name: Optional[str] = None,
               handler: Optional[PatchHandler] = None,
               priority_hint: Optional[int] = None,
               enabled: bool = True,
               apply: bool = True) -> types.FunctionType:
    """
    Specifies a bytecode-level transpiler hook.

    target_object: The object that the target function belongs to.
    target_function_name: The attribute name of the function to patch, which belongs to target_object.
    patch_name: The name of this specific patch. Used for logging
    handler: The PatchHandler to associate this hook with. If not supplied, the patch will be assigned to the anonymous patch handler.
    priority_hint: An integer hint used by the patch library to determine the order patches should be applied in. Larger numbers have higher priority, while smaller (including negative) numbers have lower priority. Defaults to zero
    enabled: Whether or not this patch is enabled. If false, then this patch will be skipped over when evaluating which patches to apply to the target method.
    apply: Whether or not to run PatchHandler.patch_all() automatically after creating this hook.
    """
    def wrapper(func):

        __create_decorator_patch(PatchTarget(target_object, target_function_name), patch_name, priority_hint, handler, enabled, apply, transpiler_func=func)

        return func

    return wrapper


def prefix(target_object: object, target_function_name: str,
               patch_name: Optional[str] = None,
               handler: Optional[PatchHandler] = None,
               priority_hint: Optional[int] = None,
               enabled: bool = True,
               apply: bool = True) -> types.FunctionType:
    """
    Specifies a prefix hook.

    target_object: The object that the target function belongs to.
    target_function_name: The attribute name of the function to patch, which belongs to target_object.
    patch_name: The name of this specific patch. Used for logging
    handler: The PatchHandler to associate this hook with. If not supplied, the patch will be assigned to the anonymous patch handler.
    priority_hint: An integer hint used by the patch library to determine the order patches should be applied in. Larger numbers have higher priority, while smaller (including negative) numbers have lower priority. Defaults to zero
    enabled: Whether or not this patch is enabled. If false, then this patch will be skipped over when evaluating which patches to apply to the target method.
    apply: Whether or not to run PatchHandler.patch_all() automatically after creating this hook.
    """
    def wrapper(func):

        __create_decorator_patch(PatchTarget(target_object, target_function_name), patch_name, priority_hint, handler, enabled, apply, prefix_func=func)

        return func

    return wrapper


def postfix(target_object: object, target_function_name: str,
               patch_name: Optional[str] = None,
               handler: Optional[PatchHandler] = None,
               priority_hint: Optional[int] = None,
               enabled: bool = True,
               apply: bool = True) -> types.FunctionType:
    """
    Specifies a postfix hook.

    target_object: The object that the target function belongs to.
    target_function_name: The attribute name of the function to patch, which belongs to target_object.
    patch_name: The name of this specific patch. Used for logging
    handler: The PatchHandler to associate this hook with. If not supplied, the patch will be assigned to the anonymous patch handler.
    priority_hint: An integer hint used by the patch library to determine the order patches should be applied in. Larger numbers have higher priority, while smaller (including negative) numbers have lower priority. Defaults to zero
    enabled: Whether or not this patch is enabled. If false, then this patch will be skipped over when evaluating which patches to apply to the target method.
    apply: Whether or not to run PatchHandler.patch_all() automatically after creating this hook.
    """
    def wrapper(func):

        __create_decorator_patch(PatchTarget(target_object, target_function_name), patch_name, priority_hint, handler, enabled, apply, postfix_func=func)

        return func

    return wrapper
