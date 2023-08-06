# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import datetime
import os
import sys
import typing as tp
from pathlib import Path

from .._logging import logger
from .._parser import ConfigParser
from .._parser import Jinja2Parser
from .._proto_namespace import _ProtoNamespace
from ._02_base import BaseComponent


class ProjectMixin(BaseComponent):
    def templated(self) -> None:
        super().templated()
        data = self.auxcon.setdefault("project", _ProtoNamespace())
        data.creation_year = self.get_current_year()

    def demodata(self) -> None:
        super().demodata()
        data = self.auxcon.project
        data.name = "hallo.world"
        data.slug = "hlw"
        data.minimal_version = (self.deduce_python_version(),)
        data.author = "anonymous"
        data.license = "MIT"

    def formatted(self) -> None:
        super().formatted()
        keys = [
            "name",
            "slug",
            "author",
            "minimal_version",
            "supported_versions",
            "creation_year",
            "source_dir",
            "license",
            "project_urls",
        ]
        self._copy_keys_over(keys, "project")
        self._to_list("project", "project_urls")

    def defaulted(self) -> None:
        # pylint: disable=no-member
        super().defaulted()
        data = self.auxd.project
        defaults = dict(
            source_dir="source",
            license="Proprietary",
            project_urls=_ProtoNamespace(),
            supported_versions=[self.auxf.project.minimal_version],
        )
        for key, val in defaults.items():
            data.setdefault(key, val)

    def enriched(self) -> None:
        super().enriched()
        data = self.auxe.project
        data.minimal_version_slug = data.minimal_version.replace(".", "")
        data.module_dir = data.source_dir + "/" + data.name.replace(".", "/")
        data.namespace_name, data.second_name = "", data.name
        if "." in data.name:
            data.namespace_name, data.second_name = data.name.split(".", 1)
        data.active_years = self.get_active_years()
        data.setup_fields = [
            "name",
            "author",
            "license",
            "description",
            "long_description",
            "project_urls",
        ]
        data.version, _ = self.get_current_version_and_lines(data)
        data.release_notes = self.get_release_notes(data)

    def bake(self) -> None:
        super().bake()
        data = self.auxe.project
        self.bake_file("install-dev.sh", chmod=0o755)
        self.bake_file("root/_setup.py", "../setup.py")

        srcj = self.root / "root/setup.cfg.jinja2"
        with Jinja2Parser.render_to_tmp(srcj, aux=self.auxe) as src:
            data.config = ConfigParser.read(src)
            for key in data.setup_fields:
                if key not in data:
                    continue
                val = data[key]
                if val:
                    data.config.metadata[key] = val

        # license
        if data.license != "Proprietary":
            self.bake_file(
                f"license/{data.license}.txt",
                (self.target / ".." / "LICENSE.txt").resolve(),
            )

    def writeout(self) -> None:
        super().writeout()
        dest = self.target / "../setup.cfg"
        written = ConfigParser.write(self.auxe.project.pop("config"), dest)
        if written:
            self._print(f"baked {dest}", fg="green")

    @classmethod
    def deduce_project_name(cls, path: tp.Optional[Path] = None) -> str:
        path = path or (Path.cwd())

        # level 1
        for obj in path.glob("*/__init__.py"):
            if "__version__" in obj.open("r", encoding="utf-8").read():
                lvl1 = obj.parent.stem
                return lvl1
        # level 2
        for obj in path.glob("*/*/__init__.py"):
            if "__version__" in obj.open("r", encoding="utf-8").read():
                lvl1 = obj.parent.stem
                lvl2 = obj.parent.parent.stem
                if lvl2 in ["source"]:
                    return lvl1
                return f"{lvl2}.{lvl1}"
        return "not-found"

    @classmethod
    def deduce_project_slug(cls) -> str:
        proj_name = cls.deduce_project_name()
        if proj_name.count(".") == 1:
            ns, sub = proj_name.split(".")
            return ns[:2] + sub[:3]
        return proj_name[:3]

    @classmethod
    def deduce_python_version(cls) -> str:
        return ".".join(map(str, sys.version_info[:2]))

    @classmethod
    def deduce_user(cls) -> str:
        return os.environ.get("USER", os.environ.get("USERNAME", "unknown"))

    def get_active_years(self) -> str:
        current_year = self.get_current_year()
        creation_year = self.auxd.project.creation_year
        if creation_year == current_year:
            return f"{creation_year}"

        return f"{creation_year}-{current_year}"

    @classmethod
    def get_current_year(cls) -> str:
        return str(datetime.date.today().year)

    def get_current_version_and_lines(
        self, data: tp.Optional[_ProtoNamespace] = None
    ) -> tp.Tuple[str, tp.List[str]]:
        data = data or self.auxe.project
        dir_ = data.module_dir
        init = self.auxcon_file.parent / dir_ / "__init__.py"
        if not init.exists():
            logger.warning(
                "%s/%s does not exist, retuning 'n/a' as version!", dir_, init.name
            )
            return "n/a", []

        with init.open("r", encoding="utf8") as f:
            lines = f.readlines()
            for line in lines:
                if "__version__" in line:
                    version = line.strip().split('"', 2)[1]
                    break
            else:
                raise RuntimeError(f"version not found in {init}")

        return version, lines

    def get_release_notes(
        self, data: tp.Optional[_ProtoNamespace] = None
    ) -> tp.Dict[str, str]:
        data = data or self.auxd.project
        dir_ = data.source_dir
        notes = self.auxcon_file.parent / data.source_dir / "release-notes.txt"
        release_note: tp.Dict[str, str] = {}

        if not notes.exists():
            logger.warning(
                "%s/%s does not exist, retuning n/a as version!", dir_, notes.name
            )
            return {}
        with notes.open("r", encoding="utf8") as f:
            for line in f.readlines():
                version, note = line.strip().split(" ", 1)
                release_note[version] = note

        return release_note
