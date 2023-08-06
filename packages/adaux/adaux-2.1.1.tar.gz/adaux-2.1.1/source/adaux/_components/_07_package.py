# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import typing as tp

from .._proto_namespace import _ProtoNamespace
from ._05_project import ProjectMixin


class PackageMixin(ProjectMixin):
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("include", "exclude")

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "package")
        for key in self.__keys():
            self._to_list("package", key)

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("package", _ProtoNamespace())
        for key in self.__keys():
            self.auxd.package.setdefault(key, [])

    def bake(self) -> None:
        super().bake()
        config = self.auxe.project.config
        data = self.auxe.package
        name = self.auxe.project.name

        for dkey, ckey in [
            ("include", "options.package_data"),
            ("exclude", "options.exclude_package_data"),
        ]:
            if not data[dkey]:
                continue
            config.setdefault(ckey, _ProtoNamespace())
            config[ckey][name] = data[dkey]
