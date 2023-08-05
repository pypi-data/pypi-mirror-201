import os
import sys
import ast
import git
import json
import openai
import difflib
import astunparse
from collections import defaultdict

from .parse_utils import get_defs, match_external_funcs, print_util

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


class TorchVaultError(Exception):
    pass


class TorchVault:
    def __init__(self, log_dir="./model_log", model_dir="./"):
        self.log_dir = log_dir
        self.model_dir = model_dir
        self.use_astunparse = True if sys.version_info.minor < 9 else False

    """
    log torch scheduler 
    """

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

    """
    log torch optimizer
    """

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
    add tag to model log
    """

    def add_tag(self, sha="", tag=""):
        os.makedirs(self.log_dir, exist_ok=True)
        # if commit hash is not given, use current commit hash
        if sha == "":
            repo = git.Repo(search_parent_directories=True)
            sha = repo.head.object.hexsha
            short_sha = sha[:7]
        else:
            short_sha = sha

        if os.path.exists(f"{self.log_dir}/model_{short_sha}"):
            with open(f"{self.log_dir}/model_{short_sha}", "r") as f:
                model_log = json.load(f)
        else:
            print(f"tvault error: model log with commit hash {sha} does not exist.")
            raise TorchVaultError

        if "tag" in model_log.keys():
            print(f"tvault: changing tag from {model_log['tag']} to {tag} for model {sha}")
            model_log["tag"] = tag

        model_json = json.dumps(model_log, sort_keys=True, indent=4)
        with open(f"{self.log_dir}/model_{short_sha}", "w") as f:
            f.write(model_json)

    """
    add result to model log
    """

    def add_result(self, sha="", result=0):
        os.makedirs(self.log_dir, exist_ok=True)
        # if commit hash is not given, use current commit hash
        if sha == "":
            repo = git.Repo(search_parent_directories=True)
            sha = repo.head.object.hexsha
            short_sha = sha[:7]
        else:
            short_sha = sha

        if os.path.exists(f"{self.log_dir}/model_{short_sha}"):
            with open(f"{self.log_dir}/model_{short_sha}", "r") as f:
                model_log = json.load(f)
        else:
            print(f"tvault error: model log with commit hash {sha} does not exist.")
            raise TorchVaultError

        if "result" in model_log.keys():
            print(f"tvault: changing result from {model_log['result']} to {result} for model {sha}")
            model_log["result"] = result

        model_json = json.dumps(model_log, sort_keys=True, indent=4)
        with open(f"{self.log_dir}/model_{short_sha}", "w") as f:
            f.write(model_json)

    """
    Basic logging for pytorch model.
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
        class_defs, function_defs = get_defs(self.model_dir)

        # get target module defs.
        filter_class_defs = defaultdict(lambda: "")
        for k, v in class_defs.items():
            if k.split(":")[-1] in target_modules:
                filter_class_defs[k] = v

        # find functions that we only want to track
        target_funcs = match_external_funcs(filter_class_defs)

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

    """
    Basic diff calculator between two pytorch models.
    """

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

        ret_str = print_util(diff_dict)

        with open(f"{self.log_dir}/diff_{sha1}_{sha2}", "w") as f:
            f.write(ret_str)

        return

    """
    Using the diff calculated with tvault, asks Chat-GPT for diff summary.
    Caveat: May involve hallucinations.
    """

    def ask_diff(self, sha1, sha2):
        print(
            "tvault Caveat: Chat-GPT may provide hallucinations, meaning that its summary may be wrong."
        )
        with open(f"{self.log_dir}/diff_{sha1}_{sha2}", "r") as f:
            model_diff = f.readlines()

        filter_model_diff = []
        for idx, e in enumerate(model_diff):
            if "SRC DIFF" in e:
                filter_model_diff = model_diff[idx + 2 :]
        filter_model_diff = "".join(filter_model_diff)

        print("=" * 20 + "Source Diff" + "=" * 20)
        print(filter_model_diff)
        model = "gpt-3.5-turbo"
        query = f"This is a string diff of two pytorch models. Please explain the difference of the two models. You do not need to explain model itself. Only elaborate on model differences. Only refer to diff sentences that starts with + or - signs. Do not refer to any other code parts. Explain in 3 sentences. Use bulletpoints.\n{filter_model_diff}"
        messages = [
            {
                "role": "system",
                "content": "You are a very talented machine learning engineer. Your job is to explain difference of two pytorch models in easy words. You are expected to answer in small number of sentences.",
            },
            {"role": "user", "content": query},
        ]
        response = openai.ChatCompletion.create(model=model, messages=messages)
        answer = response["choices"][0]["message"]["content"]
        print("\n\n")
        print("=" * 20 + "ChatGPT Answer" + "=" * 20)
        print(answer)
        return

    """
    find models using either commit hash, tag, or result
    """

    def find(self, condition="hash", hash="", tag="", min=0, max=100):
        if os.path.exists(self.log_dir):
            if len(os.listdir(self.log_dir)) == 0:
                print(f"tvault error: log dir is empty")
                raise TorchVaultError
            if condition == "hash":
                if os.path.exists(f"{self.log_dir}/model_{hash}"):
                    print(f"tvault: model {hash} exists!")
                else:
                    print(f"tvault: model {hash} does not exist.")
            elif condition == "tag":
                target_models = []
                for model in os.listdir(self.log_dir):
                    with open(f"{self.log_dir}/{model}", "r") as f:
                        model_log = json.load(f)
                    if "tag" in model_log.keys() and model_log["tag"] == tag:
                        target_models.append(model)
                print(f"tvault: models {target_models} match tag {tag}.")
            elif condition == "result":
                target_models = []
                for model in os.listdir(self.log_dir):
                    with open(f"{self.log_dir}/{model}", "r") as f:
                        model_log = json.load(f)
                    if "result" in model_log.keys() and min <= model_log["result"] <= max:
                        target_models.append(model)
                print(f"tvault: models {target_models} have result between {min} ~ {max}.")
            else:
                print(f"tvault error:condition other than [hash, tag, result] is not supported.")
                raise TorchVaultError
