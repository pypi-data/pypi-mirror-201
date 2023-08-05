import os
import sys
import ast
import git
import glob
import json
import openai
import difflib
import astunparse
from collections import defaultdict

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


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

    def log_scheduler(self, scheduler):
        os.makedirs(self.log_dir, exist_ok=True)
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        short_sha = sha[:7]

        if os.path.exists(f"{self.log_dir}/model_{short_sha}"):
            with open(f"{self.log_dir}/model_{short_sha}", "r") as f:
                model_log = json.load(f)
        else:
            model_log = dict()
        model_log["scheduler"] = scheduler.__str__()
        model_json = json.dumps(model_log, sort_keys=True, indent=4)

        with open(f"{self.log_dir}/model_{short_sha}", "w") as f:
            f.write(model_json)

    def log_optimizer(self, optimizer):
        os.makedirs(self.log_dir, exist_ok=True)
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        short_sha = sha[:7]

        if os.path.exists(f"{self.log_dir}/model_{short_sha}"):
            with open(f"{self.log_dir}/model_{short_sha}", "r") as f:
                model_log = json.load(f)
        else:
            model_log = dict()
        model_log["optimizer"] = optimizer.__str__()
        model_json = json.dumps(model_log, sort_keys=True, indent=4)

        with open(f"{self.log_dir}/model_{short_sha}", "w") as f:
            f.write(model_json)

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
        model_json = json.dumps(model_log, sort_keys=True, indent=4)

        with open(f"{self.log_dir}/model_{short_sha}", "w") as f:
            f.write(model_json)

    def print_util(self, diff_dict):
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

    def diff(self, sha1, sha2):
        with open(f"{self.log_dir}/model_{sha1}", "r") as f1:
            prev_model = json.load(f1)
        with open(f"{self.log_dir}/model_{sha2}", "r") as f2:
            cur_model = json.load(f2)
        diff_dict = dict()

        # 1. get model diff using string
        model_diff = [
            e
            for e in difflib.ndiff(prev_model["model"].split("\n"), cur_model["model"].split("\n"))
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
                    for e in difflib.ndiff(
                        p_source.split("\n"), cur_model["src"][p_module].split("\n")
                    )
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

        ret_str = self.print_util(diff_dict)

        with open(f"{self.log_dir}/diff_{sha1}_{sha2}", "w") as f:
            f.write(ret_str)

        return

    def ask_diff(self, sha1, sha2):
        with open(f"{self.log_dir}/diff_{sha1}_{sha2}", "r") as f:
            model_diff = f.readlines()

        model = "gpt-3.5-turbo"
        query = f"This is a string diff of two pytorch models. Please explain the difference of the two models. You do not need to explain model itself. Only elaborate on model differences. Only refer to diff sentences that starts with + or - signs. Do not refer to any other code parts. Explain in 3 sentences. Use bulletpoints.\n{model_diff}"
        messages = [
            {
                "role": "system",
                "content": "You are a very talented machine learning engineer. Your job is to explain difference of two pytorch models in easy words. You are expected to answer in small number of sentences.",
            },
            {"role": "user", "content": query},
        ]
        response = openai.ChatCompletion.create(model=model, messages=messages)
        answer = response["choices"][0]["message"]["content"]
        print(answer)
        return
