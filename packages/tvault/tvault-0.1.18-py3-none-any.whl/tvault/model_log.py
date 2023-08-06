import os
import sys
import ast
import git
import glob
import json
import astunparse
from collections import defaultdict


class TorchVault:
    def __init__(self, log_dir="./model_log", model_dir="./"):
        self.log_dir = log_dir
        self.model_dir = model_dir
        self.use_astunparse = True if sys.version_info.minor < 9 else False

    """
    From model directory, retrieves every class and function definition from .py files
    """

    def get_defs(self, model_dir):
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

    def match_external_funcs(self, class_defs):
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

    """
    Provide logging for pytorch model.
    1. Retrives target modules from pytorch model representation.
    2. Get class definition of target modules.
    3. Get external function definition of those used in target model.
    """

    def analyze_model(self, model):
        os.makedirs(self.log_dir, exist_ok=True)

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
        class_defs, function_defs = self.get_defs(self.model_dir)

        # get target module defs.
        filter_class_defs = defaultdict(lambda: "")
        for k, v in class_defs.items():
            if k.split(":")[-1] in target_modules:
                filter_class_defs[k] = v

        # find functions that we only want to track
        target_funcs = self.match_external_funcs(filter_class_defs)

        # unparse
        filter_target_class = defaultdict(lambda: "")
        for k, v in class_defs.items():
            if k.split(":")[-1] in target_modules:
                if self.use_astunparse:
                    filter_target_class[k] = astunparse.unparse(v)
                else:
                    filter_target_class[k] = ast.unparse(v)

        filter_target_funcs = defaultdict(lambda: "")
        for k, v in function_defs.items():
            if k.split(":")[-1] in target_funcs:
                if self.use_astunparse:
                    filter_target_funcs[k] = astunparse.unparse(v)
                else:
                    filter_target_funcs[k] = ast.unparse(v)

        # get git hash
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        short_sha = sha[:7]
        model_log = dict()
        model_log["model"] = model.__str__()
        model_log["src"] = dict(filter_target_class)
        model_log["external_func"] = dict(filter_target_funcs)
        model_json = json.dumps(model_log, indent=4)

        # Writing to sample.json
        with open(f"{self.log_dir}/model_{short_sha}", "w") as f:
            f.write(model_json)
