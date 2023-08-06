import inspect
import os.path
import sys
import tempfile
from enum import Enum
from importlib.util import module_from_spec, spec_from_loader
from typing import Any, Callable

from tiivad.edutest import create_file
from tiivad.file import File
from tiivad.function import Function
from tiivad.function_execution import FunctionExecution
from tiivad.help_structures import Check
from tiivad.program import Program
from tiivad.program_execution import ProgramExecution


# TODO: Refactor so that the call would be unified for all the similar ones.
# TODO: Function contains keyword vajab töötamiseks funktsiooni objekti, mida me staatiliselt kätte ei saa?


class ShowSourceLoader:
    def __init__(self, modname: str, source: str) -> None:
        self.modname = modname
        self.source = source

    def get_source(self, modname: str) -> str:
        if modname != self.modname:
            raise ImportError(modname)
        return self.source


def make_function(s: str) -> Callable[..., Any]:
    filename = tempfile.mktemp(suffix='.py')
    modname = os.path.splitext(os.path.basename(filename))[0]
    assert modname not in sys.modules
    # our loader is a dummy one which just spits out our source
    loader = ShowSourceLoader(modname, s)
    spec = spec_from_loader(modname, loader, origin=filename)
    module = module_from_spec(spec)
    # the code must be compiled so the function's code object has a filename
    code = compile(s, mode='exec', filename=filename)
    import contextlib
    with contextlib.redirect_stdout(None):
        exec(code, module.__dict__)
    # inspect.getmodule(...) requires it to be in sys.modules
    sys.modules[modname] = module
    return module


def string_contains_string(str, str2):
    return str in str2


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"


def program_imports_module_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    prog = Program(program_name=kwargs["file_name"])

    for check in kwargs["generic_checks"]:
        test_result, error_msg = prog.program_imports_module2(check.check_type, check.expected_value,
                                                              check.nothing_else, check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] = kwargs["generic_checks"]
    return kwargs


def program_calls_function_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    prog = Program(program_name=kwargs["file_name"])

    for check in kwargs["generic_checks"]:
        test_result, error_msg = prog.program_calls_function2(check.check_type, check.expected_value,
                                                              check.nothing_else, check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            break
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] = kwargs["generic_checks"]
    return kwargs


def program_contains_loop_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    test_result, error_msg = prog.program_contains_loop(kwargs["failed_message"])
    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]

    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def program_contains_try_except_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    test_result, error_msg = prog.program_contains_try_except(kwargs["failed_message"])
    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]

    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def program_calls_print_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    test_result, error_msg = prog.program_calls_print(kwargs["failed_message"])
    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]
    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def program_defines_function_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    prog = Program(program_name=kwargs["file_name"])

    for check in kwargs["generic_checks"]:
        test_result, error_msg = prog.program_defines_function2(check.check_type, check.expected_value,
                                                                check.nothing_else, check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            break
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] = kwargs["generic_checks"]
    return kwargs


def program_contains_keyword_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    prog = Program(program_name=kwargs["file_name"])

    for check in kwargs["generic_checks"]:
        test_result, error_msg = prog.program_contains_keyword2(check.check_type, check.expected_value,
                                                                check.nothing_else, check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            break
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] = kwargs["generic_checks"]
    return kwargs


def program_execution_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    kwargs["checks"] = []

    for file in kwargs["input_files"]:
        create_file(file[0], file[1])

    prog = Program(program_name=kwargs["file_name"])
    user_inputs = kwargs["standard_input_data"]
    pe = ProgramExecution(prog, user_inputs)

    try:
        res, _ = pe.program_execution_and_input_count()
        if not res:
            raise
    except:
        kwargs["exception_message"] = pe.program_error_message
        kwargs["test_status"] = TestResult.FAIL.name
        check = Check()
        check.error_message = pe.program_error_message
        check.check_status = TestResult.FAIL.name
        kwargs["checks"] += [check]
        return kwargs

    if pe.io_cap:
        kwargs["actual_output"] = pe.io_cap.get_stdout()
    else:
        kwargs["actual_output"] = ""

    # Standard output checks
    for check in kwargs["generic_checks"]:
        test_result, error_msg = prog.program_output_contains_keyword2(check.check_type, check.expected_value,
                                                                       check.nothing_else, kwargs["actual_output"],
                                                                       check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            kwargs["checks"] += kwargs["generic_checks"]
            return kwargs
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] += kwargs["generic_checks"]

    # Output file output checks
    for check in kwargs["output_file_checks"]:
        output_file_name = check.file_name
        file_output = File(output_file_name).get_file_text()
        test_result, error_msg = prog.program_output_contains_keyword2(check.check_type, check.expected_value,
                                                                       check.nothing_else, file_output,
                                                                       check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            kwargs["checks"] += kwargs["output_file_checks"]
            return kwargs
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] += kwargs["output_file_checks"]

    threw_error = pe.program_threw_error
    must_not_throw = kwargs["exception_check"]

    # Default check for the case when program executed successfully
    check = Check()
    check.before_message = kwargs["name"]
    check.passed_message = "Programmi käivitus õnnestus"  # TODO: Set as default
    check.failed_message = "Programmi käivitus ebaõnnestus"  # TODO: Set as default

    if not must_not_throw and not threw_error or must_not_throw and threw_error:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = pe.program_error_message
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] += [check]
    return kwargs


def function_contains_loop_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    test_result, error_msg = f.function_contains_loop(kwargs["failed_message"])
    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]

    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def function_contains_keyword_test(**kwargs):
    kwargs["test_status"] = TestResult.FAIL.name

    # TODO: FIXME:
    return

    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    func = make_function(prog.file.get_file_text())
    fu = getattr(func, f_name)
    function_string = inspect.getsource(fu)

    for check in kwargs["generic_checks"]:
        test_result, error_msg = f.function_contains_keyword2(check.check_type, check.expected_value,
                                                              check.nothing_else, function_string, check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            break
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] = kwargs["generic_checks"]
    return kwargs


def function_contains_return_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    test_result, error_msg = f.function_contains_return(kwargs["failed_message"])
    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]

    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def function_calls_function_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    for check in kwargs["generic_checks"]:
        test_result, error_msg = f.function_calls_function2(check.check_type, check.expected_value,
                                                            check.nothing_else, check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            break
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] = kwargs["generic_checks"]
    return kwargs


def function_is_recursive_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    test_result, error_msg = f.function_is_recursive(kwargs["failed_message"])
    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]

    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def function_calls_print_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    test_result, error_msg = f.function_calls_print(kwargs["failed_message"])
    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]

    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def function_defines_function_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    for check in kwargs["generic_checks"]:
        test_result, error_msg = f.function_defines_function2(check.check_type, check.expected_value,
                                                              check.nothing_else, check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            break
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] = kwargs["generic_checks"]
    return kwargs


def function_imports_module_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    for check in kwargs["generic_checks"]:
        test_result, error_msg = f.function_imports_module2(check.check_type, check.expected_value,
                                                            check.nothing_else, check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] = kwargs["generic_checks"]
    return kwargs


def function_contains_try_except_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    test_result, error_msg = f.function_contains_try_except(kwargs["failed_message"])

    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]

    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def function_is_pure_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name

    prog = Program(program_name=kwargs["file_name"])
    f_name = kwargs["function_name"]
    f = Function(f_name, prog.get_syntax_tree())

    test_result, error_msg = f.function_is_pure(kwargs["failed_message"])

    must_not_contain = kwargs["contains_check"]

    check = Check()
    check.before_message = kwargs["before_message"]
    check.passed_message = kwargs["passed_message"]
    check.failed_message = kwargs["failed_message"]

    if not must_not_contain and not test_result or must_not_contain and test_result:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.check_status = TestResult.FAIL.name
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] = [check]
    return kwargs


def function_execution_test(**kwargs):
    kwargs["test_status"] = TestResult.PASS.name
    kwargs["checks"] = []

    for file in kwargs["input_files"]:
        create_file(file[0], file[1])

    prog = Program(program_name=kwargs["file_name"])
    user_inputs_prog = kwargs["standard_input_data"]
    pe = ProgramExecution(prog, user_inputs_prog)
    f_name = kwargs["function_name"]

    try:
        res, _ = pe.program_execution_and_input_count()
        if not res:
            raise
    except:
        kwargs["exception_message"] = pe.program_error_message
        kwargs["test_status"] = TestResult.FAIL.name
        check = Check()
        check.error_message = pe.program_error_message
        check.check_status = TestResult.FAIL.name
        kwargs["checks"] += [check]
        return kwargs

    f_obj = pe.globals_dict.get(f_name, None)
    user_inputs_fun = kwargs["arguments"]
    fe = FunctionExecution(f_obj, user_inputs_fun, user_inputs_prog, kwargs["return_value"])

    try:
        fe.function_execution_and_input_count()
    except:
        # TODO: Think about this logic here
        pass

    check = Check()
    check.before_message = kwargs.get("before_message", kwargs.get("name", ""))
    check.passed_message = kwargs.get("passed_message", "")
    check.failed_message = kwargs.get("failed_message", "")
    test_result, error_msg = fe.function_return_value_correct()
    if test_result is False:
        kwargs["test_status"] = TestResult.FAIL.name
        check.error_message = error_msg
        check.failed_message = error_msg if check.failed_message == "" else check.failed_message
        check.check_status = TestResult.FAIL.name
        kwargs["checks"] += [check]
        return kwargs
    else:
        check.check_status = TestResult.PASS.name

    kwargs["checks"] += [check]

    kwargs["actual_output"] = fe.io_cap.get_stdout()

    # Standard output checks
    for check in kwargs["generic_checks"]:
        test_result, error_msg = fe.function_output_correct2(validation_type=check.check_type,
                                                             outputs=check.expected_value,
                                                             nothing_else=check.nothing_else,
                                                             actual_output=kwargs["actual_output"],
                                                             failed_message=check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            kwargs["checks"] += kwargs["generic_checks"]
            return kwargs
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] += kwargs["generic_checks"]

    # Output file output checks
    for check in kwargs["output_file_checks"]:
        output_file_name = check.file_name
        file_output = File(output_file_name).get_file_text()
        test_result, error_msg = prog.program_output_contains_keyword2(check.check_type, check.expected_value,
                                                                       check.nothing_else, file_output,
                                                                       check.failed_message)
        if not test_result:
            check.error_message = error_msg
            check.check_status = TestResult.FAIL.name
            kwargs["test_status"] = TestResult.FAIL.name
            kwargs["checks"] += kwargs["output_file_checks"]
            return kwargs
        else:
            check.check_status = TestResult.PASS.name

    kwargs["checks"] += (kwargs["output_file_checks"])
    return kwargs
