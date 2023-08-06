# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import typing as tp

from .._proto_namespace import _ProtoNamespace
from ._05_project import ProjectMixin
from ._06_dependency import DependencyMixin


class ExecutablesMixin(DependencyMixin, ProjectMixin):
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("console_scripts", "scripts")

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "executables")
        for key in self.__keys():
            self._to_list("executables", key)

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("executables", _ProtoNamespace())
        for key in self.__keys():
            self.auxd.executables.setdefault(key, [])

    def demodata(self) -> None:
        super().demodata()
        data = self.auxcon.executables
        data.scripts = ["scripts/say_hello"]

    def bake(self) -> None:
        super().bake()
        config = self.auxe.project.config
        data = self.auxe.executables

        config.options.scripts = data.scripts
        cscr = data.console_scripts
        for i, val in enumerate(cscr):
            if "=" in val:
                continue
            name = val.rsplit(":", 1)[1]
            cscr[i] = f"{name} = {val}"

        config["options.entry_points"].console_scripts = cscr
