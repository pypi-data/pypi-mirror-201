import os
import sys
import ast
import git
import json
import openai
import difflib
import astunparse
from collections import defaultdict

from .parse_utils import match_external_funcs, extract_info_from_model, extract_diff

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


class TorchVaultError(Exception):
    pass


class TorchVault:
    def __init__(self, log_dir="./model_log", model_dir="./"):
        self.log_dir = log_dir
        self.model_dir = model_dir
        self.use_astunparse = True if sys.version_info.minor < 9 else False

        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        short_sha = sha[:7]
        self.sha = short_sha
        os.makedirs(self.log_dir, exist_ok=True)

    """
    reads model log from git hash
    returns empty model_log if nothing logged
    """

    def read_model_log(self, sha=""):
        if sha == "":
            sha = self.sha

        if os.path.exists(f"{self.log_dir}/model_{sha}"):
            with open(f"{self.log_dir}/model_{sha}", "r") as f:
                import ipdb

                ipdb.set_trace()
                model_log = defaultdict(lambda: dict(), json.load(f))
                print(f"load existing model: {json.load(f)}")
        else:
            model_log = defaultdict(lambda: dict())
        return model_log

    """
    write model log to git hash
    """

    def write_model_log(self, sha="", model_log=defaultdict(lambda: dict())):
        if sha == "":
            sha = self.sha
        with open(f"{self.log_dir}/model_{sha}", "w") as f:
            json.dump(dict(model_log))

    """
    log torch scheduler 
    """

    def log_scheduler(self, scheduler):
        model_log = self.read_model_log()
        model_idx = len(model_log.keys()) - 1
        print(f"model idx - add scheduler: {model_idx}")
        model_log[model_idx]["scheduler"] = scheduler.__str__()
        self.write_model_log("", model_log)

    """
    log torch optimizer
    """

    def log_optimizer(self, optimizer):
        model_log = self.read_model_log()
        model_idx = len(model_log.keys()) - 1
        print(f"model idx - add optimizer: {model_idx}")
        model_log[model_idx]["optimizer"] = optimizer.__str__()
        self.write_model_log("", model_log)

    """
    add tag to model log, commit sha may be from previous results.
    if idx is set to -1, all models in the commit hash are tagged.
    if idx is set to None, tag of most recent model is changed.
    """

    def add_tag(self, sha="", tag="", idx=None):
        # if commit hash is not given, use current commit hash
        model_log = self.read_model_log(sha)
        print(f"add tag: got model_log {model_log}")
        if len(model_log.keys()) == 0:
            print(f"tvault error: model log with commit hash {sha} does not exist.")
            raise TorchVaultError

        if idx == -1:
            target_idxs = list(range(len(model_log.keys())))
        elif idx == None:
            target_idxs = [len(model_log.keys()) - 1]
            print(f"add tags: {target_idxs}")
        else:
            target_idxs = [idx]

        for model_idx in target_idxs:
            if "tag" in model_log[model_idx].keys():
                print(
                    f"tvault: changing tag from {model_log[model_idx]['tag']} to {tag} for model {sha}"
                )
            else:
                print(f"tvault: setting tag {tag} for model {sha}")
            model_log[model_idx]["tag"] = tag
        print(f"write log: {model_log}")
        self.write_model_log(sha, model_log)

    """
    add result to model log, commit sha may be from previous results.
    if idx is set to -1, all models in the commit hash are tagged.
    if idx is set to None, tag of most recent model is changed.
    """

    def add_result(self, sha="", result=0, idx=None):
        # if commit hash is not given, use current commit hash
        model_log = self.read_model_log(sha)
        print(f"add tag: got model_log {model_log}")
        if len(model_log.keys()) == 0:
            print(f"tvault error: model log with commit hash {sha} does not exist.")
            raise TorchVaultError

        if idx == -1:
            target_idxs = list(range(len(model_log.keys())))
        elif idx == None:
            target_idxs = [len(model_log.keys()) - 1]
            print(f"add results: {target_idxs}")
        else:
            target_idxs = [idx]

        for model_idx in target_idxs:
            if "result" in model_log[model_idx].keys():
                print(
                    f"tvault: changing result from {model_log[model_idx]['result']} to {result} for model {sha}"
                )
            else:
                print(f"tvault: setting result {result} for model {sha}")
            model_log[model_idx]["result"] = result
        print(f"write log: {model_log}")
        self.write_model_log(sha, model_log)

    """
    Basic logging for pytorch model.
    1. Retrives target modules from pytorch model representation.
    2. Get class definition of target modules.
    3. Get external function definition of those used in target model.

    Each logged model is stacked using index.
    """

    def log_model(self, model):
        class_defs, function_defs, target_modules = extract_info_from_model(model, self.model_dir)

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

        model_log = self.read_model_log()
        model_idx = len(model_log.keys())
        print(f"model idx: {model_idx}")
        model_log[model_idx]["model"] = model.__str__()
        model_log[model_idx]["src"] = dict(filter_target_class)
        model_log[model_idx]["external_func"] = dict(filter_target_funcs)
        print(f"write model in model log {model_log}")
        self.write_model_log("", model_log)

    """
    Basic diff calculator between two pytorch models.
    sha1: commit hash of previous model, must be set. (for now)
    index1: model index of model in commit hash sha1. If not set, use latest.
    sha2: commit hash of current model, must be set. (for now)
    index2: model index of model in commit hash sha2. If not set, use latest.
    out: if out flag is set, writes out
    ask_gpt: if ask_gpt is set, asks gpt for difference summary.
    """

    def diff(self, sha1="", index1=-1, sha2="", index2=-1, out=False, ask_gpt=False):
        prev_model = self.read_model_log(sha1)
        cur_model = self.read_model_log(sha2)
        if len(prev_model.keys()) == 0:
            print(f"tvault error: sha1 argument must be provided.")
        if len(cur_model.keys()) == 0:
            print(f"tvault error: sha2 argument must be provided.")
        if index1 == -1:
            index1 = len(prev_model.keys()) - 1
        if index2 == -1:
            index2 = len(cur_model.keys()) - 1

        prev_model = prev_model[index1]
        cur_model = cur_model[index2]

        ret_str, diff_dict = extract_diff(prev_model, cur_model)

        if out:
            with open(f"{self.log_dir}/diff_{sha1}_{sha2}", "w") as f:
                f.write(ret_str)
        print(ret_str)

        if ask_gpt:
            self.ask_diff(diff_dict)

        return

    """
    Using the diff calculated with tvault, asks Chat-GPT for diff summary.
    Caveat: May involve hallucinations.
    """

    def ask_diff(self, diff_dict):
        print(
            "tvault Caveat: Chat-GPT may provide hallucinations, meaning that its summary may be wrong."
        )

        feed_gpt = ""

        if len(diff_dict["src"].keys()) > 0:
            for k, v in diff_dict["src"].items():
                feed_gpt += v + "\n"

        if len(diff_dict["func"].keys()) > 0:
            for k, v in diff_dict["func"].items():
                feed_gpt += v + "\n"

        print("=" * 20 + "Source Diff" + "=" * 20)
        print(feed_gpt)
        model = "gpt-3.5-turbo"
        query = f"This is a string diff of two pytorch models. Please explain the difference of the two models. You do not need to explain model itself. Only elaborate on model differences. Only refer to diff sentences that starts with + or - signs. Do not refer to any other code parts. Use bulletpoints.\n{feed_gpt}"
        messages = [
            {
                "role": "system",
                "content": "You are a very talented machine learning engineer. Your job is to explain difference of two pytorch models in easy words. You are expected to answer in smallest number of senteces as possible.",
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
                if hash == "":
                    print(f"tvault error: hash is not set for hash finding")
                    raise TorchVaultError
                if os.path.exists(f"{self.log_dir}/model_{hash}"):
                    model_log = self.read_model_log(hash)
                    print(
                        f"tvault: model {hash} exists! - contains {len(model_log.keys())} experiments"
                    )
                else:
                    print(f"tvault: model {hash} does not exist.")
            elif condition == "tag":
                target_models = []
                for model in os.listdir(self.log_dir):
                    with open(f"{self.log_dir}/{model}", "r") as f:
                        model_log = json.load(f)
                    for model_idx, v in model_log.items():
                        if "tag" in v.keys() and v["tag"] == tag:
                            target_models.append([model, model_idx])
                print(f"tvault: models {target_models} match tag {tag}.")
            elif condition == "result":
                target_models = []
                for model in os.listdir(self.log_dir):
                    with open(f"{self.log_dir}/{model}", "r") as f:
                        model_log = json.load(f)
                    for model_idx, v in model_log.items():
                        if "result" in v.keys() and min <= v["result"] <= max:
                            target_models.append([model, model_idx])
                print(f"tvault: models {target_models} have result between {min} ~ {max}.")
            else:
                print(f"tvault error:condition other than [hash, tag, result] is not supported.")
                raise TorchVaultError
