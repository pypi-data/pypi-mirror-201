# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import copy
import os
import subprocess
import sys
import typing as tp
from pathlib import Path

from .._parser import ConfigParser
from .._proto_namespace import _ProtoNamespace
from ._03_meta import MetaMixin
from ._06_dependency import DependencyMixin


class PylintMixin(DependencyMixin, MetaMixin):
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return (
            "disable",
            "good_names",
            "class_attr_rgx",
            "min_similarity_lines",
            "argument_rgx",
            "function_rgx",
            "variable_rgx",
            "method_rgx",
        )

    def templated(self) -> None:
        super().templated()
        data = self.auxcon.pylint = _ProtoNamespace()
        self.auxcon.dependencies.dev.append(self.versions.pylint)
        data.disable = [
            "use-dict-literal",
            "too-few-public-methods",
            "line-too-long",
            "wrong-import-position",
            "wildcard-import",
        ]
        if not self.is_enabled("docs"):
            data.disable += [
                "missing-class-docstring",
                "missing-module-docstring",
                "missing-function-docstring",
            ]

    def demodata(self) -> None:
        super().demodata()
        data = self.auxcon.pylint
        data.setdefault("disable", [])
        data.disable += ["too-few-public-methods", "no-self-use"]
        data.good_names = ["t", "dt"]

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "pylint")
        self._copy_keys_over(self.__keys(), "pylint_test")
        for key in self.__keys()[:2]:
            self._to_list("pylint", key)
            self._to_list("pylint_test", key)

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("pylint", _ProtoNamespace())
        self.auxd.setdefault("pylint_test", _ProtoNamespace())
        for key in self.__keys()[:2]:
            self.auxd.pylint.setdefault(key, [])
            self.auxd.pylint_test.setdefault(key, [])

    def bake(self) -> None:  # pylint: disable=too-many-locals,too-many-branches
        super().bake()
        # ensure python version
        found_version = ".".join(map(str, sys.version_info[:2]))
        if found_version != self.auxe.project.minimal_version:
            raise RuntimeError(
                f"you are using python {found_version}, please use python {self.auxe.project.minimal_version} (minimal version)."
            )

        # the home of the user has a potential .pylintrc file,
        # which will influence the creation
        env = os.environ.copy()
        pylint_rc = Path(os.environ["HOME"]) / ".pylintrc"
        if pylint_rc.exists():
            env["HOME"] = "/tmp"
        resp = subprocess.run(
            ["pylint", "--generate-rcfile"], capture_output=True, check=True, env=env
        )
        text = resp.stdout.decode()

        hooks = self.auxe.pre_commit.hooks
        configs = [ConfigParser.read_string(text)]
        keys = ["pylint"]
        writeout = ["pylint" in hooks]

        writeout.append("pylint-test" in hooks)
        if writeout[-1]:
            keys.append("pylint-test")

        for i, key in enumerate(keys):
            config = configs[-1]
            if i > 0:
                config = copy.deepcopy(config)
                configs.append(config)

            key = key.replace("-", "_")
            for key1, key2, key3 in [
                ("MESSAGES CONTROL", "disable", "disable"),
                ("BASIC", "good-names", "good_names"),
                ("SIMILARITIES", "min-similarity-lines", "min_similarity_lines"),
                ("BASIC", "variable-rgx", "variable_rgx"),
                ("BASIC", "const-rgx", "const_rgx"),
                ("BASIC", "function-rgx", "function_rgx"),
                ("BASIC", "argument-rgx", "argument_rgx"),
                ("BASIC", "class-rgx", "class_rgx"),
                ("BASIC", "method-rgx", "method_rgx"),
                ("BASIC", "attr-rgx", "attr_rgx"),
                ("BASIC", "class-attribute-rgx", "class_attr_rgx"),
            ]:
                subconfig = config[key1]
                data = self.auxe[key]
                if key2 in ["good-names", "disable"]:
                    proplist = copy.copy(subconfig[key2])
                    for x in data[key3]:
                        proplist[-1] += ","
                        if x in proplist:
                            raise RuntimeError(f"{x} is already marked {key3}")
                        proplist.append(x)
                    subconfig[key2] = proplist
                else:
                    if key3 in data:
                        subconfig[key2] = data[key3]

            config["SIMILARITIES"]["ignore-imports"] = "yes"

        for key, config, wout in zip(keys, configs, writeout):
            if not wout:
                continue
            dest = self.target / f"pre-commit/{key}rc"
            written = ConfigParser.write(config, dest)
            if written:
                self._print(f"baked {dest}", fg="green")
