# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import typing as tp
from pathlib import Path

from .._parser import ConfigParser
from .._proto_namespace import _ProtoNamespace
from ._06_dependency import DependencyMixin


class MypyMixin(DependencyMixin):
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("ignore",)

    def templated(self) -> None:
        super().templated()
        self.auxcon.dependencies.dev.append(self.versions.mypy)

    def demodata(self) -> None:
        super().demodata()
        self.auxcon.mypy = _ProtoNamespace(ignore=["click_help_colors"])

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "mypy")
        for key in self.__keys():
            self._to_list("mypy", key)

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("mypy", _ProtoNamespace())
        for key in self.__keys():
            self.auxd.mypy.setdefault(key, [])

    def bake(self) -> None:
        super().bake()
        src = self.root / "pre-commit/mypy.ini"
        dest = self.target / "pre-commit/mypy.ini"
        config = ConfigParser.read(src)

        # namespace compat
        if "." in self.auxe.project.name:
            config["mypy"]["namespace_packages"] = True
            config["mypy"]["explicit_package_bases"] = True
            config["mypy"][
                "mypy_path"
            ] = f"$MYPY_CONFIG_FILE_DIR/../../{self.auxe.project.source_dir}"

        for x in self.auxe.mypy.ignore:
            config[f"mypy-{x}.*"] = _ProtoNamespace(ignore_missing_imports="True")

        # special django stubs case
        for dep in self.auxe.dependencies["dev"]:
            if (
                "django-stubs" in dep
                and (Path(self.auxe.project.source_dir) / "settings.py").exists()
            ):
                config["mypy"]["plugins"] = ["mypy_django_plugin.main"]
                config["mypy.plugins.django-stubs"] = dict(
                    django_settings_module=f"{self.auxe.project.name}.settings"
                )

        written = ConfigParser.write(config, dest)
        if written:
            self._print(f"baked {dest}", fg="green")
