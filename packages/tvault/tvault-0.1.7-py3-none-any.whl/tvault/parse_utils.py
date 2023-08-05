import ast
import glob
from collections import defaultdict


"""
From model directory, retrieves every class and function definition from .py files
"""


def get_defs(model_dir):
    function_defs = defaultdict(lambda: "")
    class_defs = defaultdict(lambda: "")
    for filename in glob.iglob(model_dir + "**/*.py", recursive=True):
        with open(filename, "r") as f:
            file_ast = ast.parse(f.read())
        for stmt in file_ast.body:
            if type(stmt) == ast.ClassDef:
                class_defs[filename + ":" + stmt.name] = stmt
            elif type(stmt) == ast.FunctionDef:
                function_defs[filename + ":" + stmt.name] = stmt
    return class_defs, function_defs


"""
From class definitions, retrieve function names that are not class methods from __init__.
"""


def match_external_funcs(class_defs):
    target_funcs = []
    for class_def in class_defs.values():
        # for each body in class definitions,
        for body in class_def.body:
            try:
                # if the function is __init__,
                if body.name == "__init__":
                    init_body = body
                    # for each stmt in init_body,
                    for stmt in init_body.body:
                        # external if satisfies following condition
                        if (
                            type(stmt) == ast.Assign
                            and type(stmt.value) == ast.Call
                            and type(stmt.value.func) == ast.Name
                        ):
                            # this is the function we need to track
                            function_name = stmt.value.func.id
                            target_funcs.append(function_name)
            # parsing errors will happen by default
            except:
                pass
    return list(set(target_funcs))


def print_util(diff_dict):
    large_space = 40
    space = 30
    ret_str = ""

    ret_str += "=" * large_space + "MODEL DIFF" + "=" * large_space + "\n"
    ret_str += diff_dict["model"] + "\n"

    if len(diff_dict["src"].keys()) > 0:
        ret_str += "=" * large_space + "SRC DIFF" + "=" * large_space + "\n"
        for k, v in diff_dict["src"].items():
            ret_str += "=" * space + f"{k}" + "=" * space + "\n"
            ret_str += v + "\n"

    if len(diff_dict["func"].keys()) > 0:
        ret_str += "=" * large_space + "FUNC DIFF" + "=" * large_space + "\n"
        for k, v in diff_dict["func"].items():
            ret_str += "=" * space + f"{k}" + "=" * space + "\n"
            ret_str += v + "\n"
    return ret_str
