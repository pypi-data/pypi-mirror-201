# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import io
import shutil
import subprocess
import sys
import typing as tp
from pathlib import Path

from ._components import AllComponents
from ._components import ExtraLevel
from ._components._02_base import BaseComponent
from ._components._03_meta import MetaMixin
from ._components._98_sentinel import SentinelMixin
from ._gitlab import GitlabSetter
from ._proto_namespace import _ProtoNamespace
from ._tick import TickSetter
from ._todo import TodoSetter
from ._util import LazyVersionStr


class CliMixin(  # pylint: disable=too-many-public-methods
    SentinelMixin, MetaMixin, BaseComponent
):
    def __init__(self, target: Path, silent: bool = False) -> None:
        super().__init__()
        self.verbose = not silent
        self.target = Path(target or "devops").resolve()

        if str(Path.cwd()) in str(self.target):
            self.target = self.target.relative_to(Path.cwd())

        valid_suffix = [".yml", ".yaml", ".cfg"]
        candidates = [
            (self.target.parent / "auxilium").with_suffix(sfx) for sfx in valid_suffix
        ]
        self.auxcon_file = candidates[0]

        # fuzzy finder via git root
        if not any(cand.exists() for cand in candidates) and target is None:
            resp = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                check=False,
            )
            if resp.returncode == 0:
                git_root = Path(resp.stdout.decode().strip())
                self.target = git_root / "devops"
                candidates = [
                    (git_root / "auxilium").with_suffix(sfx) for sfx in valid_suffix
                ]

        for cand in candidates:
            if cand.exists():
                self.auxcon_file = cand
                self.load_auxcon()
                break
        self._print(f"adaux {LazyVersionStr()} at your service", fg="blue")

    def demo(self: "CliMixin") -> None:
        out = io.StringIO()
        self.save_auxcon_to_stream(out, level=ExtraLevel.DEMODATA)
        self._print(out.getvalue())

    def show(self: "CliMixin", full: bool = False) -> None:
        out = io.StringIO()
        self.save_auxcon_to_stream(
            out, level=ExtraLevel.ENRICHED if full else ExtraLevel.DEFAULTED
        )
        self._print(out.getvalue())

    def init(  # pylint: disable=too-many-arguments
        self: "CliMixin",
        project_name: str,
        project_slug: str,
        python_version: str,
        author: str,
        force: bool = False,
    ) -> None:
        self.auxcon.project = _ProtoNamespace(
            name=project_name,
            slug=project_slug,
            minimal_version=python_version,
            author=author,
        )
        self.target.mkdir(parents=True, exist_ok=True)

        self.save_auxcon_and_print(ExtraLevel.TEMPLATED, force=force)

    def save_auxcon_and_print(self, level: ExtraLevel, force: bool = False) -> None:
        dest = self.auxcon_file
        over, fg_col = "", "green"
        if dest.exists():
            if not force:
                raise RuntimeError(f"{dest} exists, use -f or --force to overwrite.")
            over, fg_col = "over", "yellow"

        with self.extra(level=level) as aux:
            self.save_auxcon(aux)

        # pylint: disable=protected-access
        self._print(f"{over}written template to {dest}", fg=fg_col)

    def sync(self: "CliMixin") -> None:
        with self.extra(ExtraLevel.FORMATTED) as aux:
            proj = aux.project
        clean: SentinelMixin = self.type_wo_disabled(discard_before="SentinelMixin")()  # type: ignore
        # full holds all possible defaults (in case something got disabled)
        full: SentinelMixin = AllComponents().type_wo_disabled(  # type: ignore
            discard_before="SentinelMixin"
        )()

        for ns in [clean, full]:
            # pylint: disable=no-member
            ns.auxcon.project = _ProtoNamespace(
                name=proj.name,
                slug=proj.slug,
                minimal_version=proj.minimal_version,
                author=proj.author,
            )

        with self.extra(ExtraLevel.FORMATTED) as aux, clean.extra(
            ExtraLevel.TEMPLATED
        ), full.extra(ExtraLevel.TEMPLATED):
            self.update_to_template(clean.auxf, full.auxf)
            self.save_auxcon(aux)

    def bake(self: "CliMixin") -> None:
        if not self.auxcon_file.exists():
            raise RuntimeError(f"{self.auxcon_file} does not exists! use 'aux init'")
        super().bake()

    def gitlab(self: "CliMixin", token: str) -> None:
        with self.extra():
            gls = GitlabSetter(self, token)  # type: ignore
            gls.bake()

    def pipeline(
        self: "CliMixin", token: str, show_success: bool
    ) -> tp.Tuple[bool, bool]:
        with self.extra():
            gls = GitlabSetter(self, token)  # type: ignore
            return gls.pipeline(show_success)

    def tick(
        self: "CliMixin",
        release_message: str,
        major: bool = False,
        minor: bool = False,
        commit: bool = False,
    ) -> None:
        if major and minor:
            raise RuntimeError("cannot set major and minor tick at the same time!")
        if len(release_message) < 16:
            raise RuntimeError("message cannot be shorter than 16 char")
        ticker = TickSetter(self, release_message, major, minor)  # type: ignore
        with self.extra():
            ticker.bake()
            if commit:
                ticker.commit()

    def release(
        self: "CliMixin", token: str, rerelease: bool = False
    ) -> tp.Tuple[bool, bool]:
        with self.extra():
            gls = GitlabSetter(self, token)  # type: ignore
            return gls.release(rerelease)

    def convert(self: "CliMixin", src: Path, dest: Path, force: bool = False) -> None:
        self.auxcon_file = src
        self.load_auxcon()
        self.auxcon_file = dest
        self.save_auxcon_and_print(ExtraLevel.DEFAULTED, force=force)

    def ci(self: "CliMixin", trigger_str: str, dry: bool = False) -> int:
        self._raise_if_disabled("ci")
        with self.extra(ExtraLevel.HYDRATED), self.cwd_to_root():
            return self.run_ci(trigger_str, dry=dry)  # type: ignore

    def cov(self: "CliMixin", open_html: bool = False) -> None:
        self._raise_if_disabled("coverage")
        cov_cache = self.target / "cache" / "coverage"
        datafile = cov_cache / "data_file"
        cov_file = self.target.parent / ".coverage"
        if datafile.exists():
            if cov_file.exists():
                datafile.unlink()
            else:
                datafile.rename(cov_file)

        with self.extra(ExtraLevel.FORMATTED) as aux:
            # pylint: disable=no-member
            cmd = [
                "pytest",
                "--cov",
                f"--cov={aux.project.name}",
                f"--cov-report=html:{cov_cache}",
            ]
            subprocess.run(cmd, check=True)
            cov_file.rename(datafile)

            if open_html:
                cmd = ["open", str(cov_cache / "index.html")]
                subprocess.run(cmd, check=True)

    def dcp(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("docker")
        cmd = [
            "docker",
            "compose",
            "-f",
            str(self.target / "docker" / "compose.yml"),
            *args,
        ]
        subprocess.run(cmd, check=False)

    def comp(self: "CliMixin", composition: str, *args: str) -> None:
        self._raise_if_disabled("docker")
        cmd = [
            "sh",
            str(self.target / "docker" / f"{composition}-compose.sh"),
            *args,
        ]
        subprocess.run(cmd, check=False)

    def run(self: "CliMixin", *payload_names: str, force: bool = False) -> None:
        self._raise_if_disabled("payload")
        with self.extra(ExtraLevel.HYDRATED), self.cwd_to_root():
            data = self.auxh.payload
            if payload_names == ("ls",):
                for title, flavor in [
                    ("payloads", "docker_build"),
                    ("with deps", "with_dependency"),
                ]:
                    list_ = list(data.lookup.level(flavor).values())
                    if not list_:
                        continue
                    self._print("=" * len(title))
                    self._print(title)
                    self._print("=" * len(title))
                    for payload in list_:
                        print("-", payload.name)

                return
            try:
                payloads = [data.lookup[x] for x in payload_names]
            except KeyError as err:
                raise RuntimeError(
                    f"payload '{payload_names}' not found! Use aux run ls, or check the {self.auxcon_file.name} file."
                ) from err
            success = self.payload_run(*payloads, force=force)  # type: ignore
            if not success:
                sys.exit(1)

    def docs(self: "CliMixin", open_html: bool = False) -> None:
        self._raise_if_disabled("docs")

        docs_cache = self.target / "cache" / "docs"

        with self.extra() as aux:
            # pylint: disable=no-member
            if aux.docs.framework == "sphinx":
                cmd = ["sphinx-apidoc", "-o", aux.docs.root, aux.project.module_dir]
                subprocess.run(cmd, check=True)
                cmd = ["sphinx-build", "-M", "html", aux.docs.root, docs_cache]
                if aux.docs.get("strict", True):
                    cmd.append("-W")
                subprocess.run(cmd, check=True)
                cmd = [
                    "python",
                    self.target / "docs" / "postprocess_html.py",
                    (docs_cache / "html" / aux.project.second_name).with_suffix(
                        ".html"
                    ),
                ]
                subprocess.run(cmd, check=True)
            elif aux.docs.framework == "mkdocs":
                cmd = ["mkdocs", "build", "-f", f"{aux.docs.root}/mkdocs.yml"]
                subprocess.run(cmd, check=True)
            else:
                raise NotImplementedError(aux.docs.framework)

        if open_html:
            cmd = ["open", docs_cache / "html" / "index.html"]
            subprocess.run(cmd, check=True)

    def mp(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("mypy")
        cmd = ["git", "add", "-u"]
        subprocess.run(cmd, check=True)
        cmd = [
            "pre-commit",
            "run",
            f"--config={self.target/'pre-commit'/'config.yaml'}",
            "mypy",
            *args,
        ]
        self._run_with_line_limit(cmd)

    def pipi(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("pip")
        optional = ""
        if args:
            optional = f'[{",".join(args)}]'
        cmd = [
            "pip",
            "install",
            "-e",
            f"{self.target.parent}{optional}",
            "--config-settings",
            "editable_mode=strict",
        ]
        subprocess.run(cmd, check=False)

    def pl(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("pylint")
        cmd = ["git", "add", "-u"]
        subprocess.run(cmd, check=True)
        cmd = [
            "pre-commit",
            "run",
            f"--config={self.target/'pre-commit'/'config.yaml'}",
            "pylint",
            *args,
        ]
        self._run_with_line_limit(cmd)

    def pra(self: "CliMixin", *args: str) -> None:
        self._raise_if_disabled("pre-commit")
        cmd = ["git", "add", "-u"]
        subprocess.run(cmd, check=True)
        if not args:
            args = ("--all",)
        cmd = [
            "pre-commit",
            "run",
            f"--config={self.target/'pre-commit'/'config.yaml'}",
            *args,
        ]
        subprocess.run(cmd, check=False)

    def sdist(self: "CliMixin", zipped: bool = False) -> None:
        self._raise_if_disabled("package")
        cmd = ["python", "setup.py", "sdist"]
        subprocess.run(cmd, check=True)

        if not zipped:
            files = list((self.target.parent / "dist").glob("*.tar.gz"))
            for file in files:
                path = file.with_name(file.name.replace(".tar.gz", ""))
                if path.exists():
                    shutil.rmtree(path, ignore_errors=True)
            cmd = ["tar", "-zxf", *map(str, files), "-C", "dist"]
            subprocess.run(cmd, check=True)
            for file in files:
                file.unlink()

    def todo_and_note(
        self: "CliMixin",
        flavor: str,
        new: tp.Optional[str] = None,
        close: tp.Optional[str] = None,
        gitignore: bool = False,
    ) -> None:
        if new and close:
            raise RuntimeError("cannot set new and close an the same time")

        with self.extra(), self.cwd_to_root():
            todo = TodoSetter(self)  # type: ignore
            if gitignore:
                todo.add_gitignore()
            if new:
                todo.new(new, flavor)
            elif close:
                todo.close(close, flavor)
            else:
                todo.show(flavor)

    def _raise_if_disabled(self, component: str) -> None:
        if not self.is_enabled(component):
            raise RuntimeError(
                f"{component} disabled for this project, check your auxilium file."
            )

    @staticmethod
    def _run_with_line_limit(cmd: tp.List[str], limit: int = 50) -> None:
        proc = subprocess.run(cmd, check=False, stdout=subprocess.PIPE)
        i = 0
        for i, line in enumerate(proc.stdout.decode("utf-8").split("\n")):
            if i < limit:
                print(line)
        if i >= limit:
            print(f"{i-limit} more lines not shown, only the first {limit}...")


class CliRenderer(CliMixin, AllComponents):  # pylint: disable=too-many-ancestors
    pass
