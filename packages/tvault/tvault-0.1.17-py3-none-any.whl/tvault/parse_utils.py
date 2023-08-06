import ast
import glob
import difflib
from collections import defaultdict

"""
extract target_modules, class_defs, function_defs from model.
"""


def extract_info_from_model(model, model_dir):
    model = model.__str__()
    target_modules = set()
    # retrieve target modules
    for line in model.split("\n"):
        if "(" in line:
            if line == line.strip():
                # model classname
                target_module = line.split("(")[0]
            else:
                # submodules
                target_module = line.split("(")[1].split(" ")[-1]
            target_modules.add(target_module)

    # retrieve class / function definitions
    class_defs, function_defs = get_defs(model_dir)
    return class_defs, function_defs, target_modules


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


def extract_diff(prev_model, cur_model):
    diff_dict = dict()
    # 1. get model diff using string
    model_diff = [
        e for e in difflib.ndiff(prev_model["model"].split("\n"), cur_model["model"].split("\n"))
    ]
    filter_model_diff = [l for l in model_diff if not l.startswith("? ")]
    model_diff = "\n".join(filter_model_diff)
    diff_dict["model"] = model_diff

    # 2. Check module definition between modules
    class_diff_dict = dict()
    for p_module, p_source in prev_model["src"].items():
        # if module still exists in current model
        if p_module in cur_model["src"].keys():
            class_diff = [
                e
                for e in difflib.ndiff(p_source.split("\n"), cur_model["src"][p_module].split("\n"))
            ]  # generator requires this wrapping
            changes = [l for l in class_diff if l.startswith("+ ") or l.startswith("- ")]
            filter_class_diff = [l for l in class_diff if not l.startswith("? ")]
            if len(changes) > 0:
                class_diff_dict[p_module] = "\n".join(filter_class_diff)
        else:
            class_diff_dict[p_module] = "module removed"
    for c_module, c_source in cur_model["src"].items():
        if c_module not in prev_model["src"].keys():
            class_diff_dict[c_module] = "module added"
    diff_dict["src"] = class_diff_dict

    # 3. Check external function diff
    func_diff_dict = dict()
    for p_func, p_source in prev_model["external_func"].items():
        if p_func in cur_model["external_func"].keys():
            func_diff = [
                e
                for e in difflib.ndiff(
                    p_source.split("\n"), cur_model["external_func"][p_func].split("\n")
                )
            ]  # generator requires this wrapping
            changes = [l for l in func_diff if l.startswith("+ ") or l.startswith("- ")]
            filter_func_diff = [l for l in func_diff if not l.startswith("? ")]
            if len(changes) > 0:
                func_diff_dict[p_func] = "\n".join(filter_func_diff)
        else:
            func_diff_dict[p_func] = "function removed"
    for c_func, c_source in cur_model["external_func"].items():
        if c_func not in prev_model["external_func"].keys():
            func_diff_dict[c_func] = "function added"
    diff_dict["func"] = func_diff_dict

    ret_str = print_util(diff_dict)

    return ret_str, diff_dict
