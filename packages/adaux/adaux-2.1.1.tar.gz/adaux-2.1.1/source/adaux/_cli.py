# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import contextlib
import os
import sys
import time
import typing as tp
from pathlib import Path

import click
from click_help_colors import HelpColorsGroup

from ._cli_mixin import CliMixin
from ._cli_mixin import LazyVersionStr
from ._components import AllComponents
from ._logging import logging

__all__ = ["adaux", "hello"]


def hello(bla: str, param: tp.Optional[click.Parameter] = None) -> str:
    r"""
    Hello:

    .. include:: example.rst
    """
    print(param)
    return bla


class _ClickPrintMixin:
    def _print(self, msg: str, **kwgs: tp.Dict[str, tp.Any]) -> None:
        if self.verbose:  # type: ignore
            click.secho(msg, **kwgs)  # type: ignore


@click.group(
    cls=HelpColorsGroup, help_headers_color="yellow", help_options_color="green"
)
@click.version_option(version=LazyVersionStr())  # type: ignore
@click.pass_context
@click.option("--target", "-t", type=Path, help="Location of the repository.")
@click.option(
    "--bake-before",
    "-b",
    is_flag=True,
    default=False,
    help="Bake before executing the command.",
)
@click.option(
    "--silent",
    "-s",
    is_flag=True,
    default=False,
    help="Suppress any output on success.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enables logging level Debug.",
)
def adaux(
    ctx: click.Context,
    target: tp.Optional[Path],
    bake_before: bool,
    silent: bool,
    verbose: bool,
) -> None:
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.INFO)
    ctx.color = os.environ.get("NO_COLOR", "") == ""
    cls = AllComponents.compose(CliMixin, _ClickPrintMixin)
    bootstrap = cls(target, True)  # type: ignore
    with convert_runtime_to_click_error():
        ctx.obj = bootstrap.type_wo_disabled()(target, silent)  # type: ignore

    if ctx.obj.auxcon_file.exists():
        raise_if_init_and_not_force(ctx)
        if bake_before:
            ctx.invoke(bake)
    else:
        raise_if_not_init(ctx)


@adaux.command()
@click.pass_context
def demo(ctx: click.Context) -> None:
    r"""
    Print a more complex auxilium file for reference.
    """
    ctx.obj.demo()


@adaux.command()
@click.pass_context
@click.option(
    "-a", "--full", is_flag=True, default=False, help="display all extra settings"
)
def show(ctx: click.Context, full: bool) -> None:
    r"""
    Read and print auxilium file in yml syntax.
    """
    with convert_runtime_to_click_error():
        ctx.obj.show(full)


@adaux.command()
@click.pass_context
@click.option("-f", "--force", is_flag=True, default=False)
@click.option(
    "-n", "--project-name", prompt=True, default=AllComponents.deduce_project_name()
)
@click.option(
    "-s", "--project-slug", prompt=True, default=AllComponents.deduce_project_slug()
)
@click.option(
    "-p", "--python-version", prompt=True, default=AllComponents.deduce_python_version()
)
@click.option("-a", "--author", prompt=True, default=AllComponents.deduce_user())
def init(  # pylint: disable=too-many-arguments
    ctx: click.Context,
    project_name: str,
    project_slug: str,
    python_version: str,
    author: str,
    force: bool,
) -> None:
    r"""
    Initialize a new auxilium.aux.
    """
    with convert_runtime_to_click_error():
        ctx.obj.init(project_name, project_slug, python_version, author, force=force)


@adaux.command()
@click.pass_context
@click.option("--bake_after", "-b", is_flag=True)
def sync(ctx: click.Context, bake_after: bool) -> None:
    r"""
    Synchronizes local auxilium file with potentially newer template.
    """
    with convert_runtime_to_click_error():
        ctx.obj.sync()

    if bake_after:
        ctx.obj.set_defaults()
        ctx.obj.bake()


@adaux.command()
@click.pass_context
def bake(ctx: click.Context) -> None:  # pylint: disable=too-many-statements
    """
    Renders various files based on an auxilium file. Will overwrite without asking.
    """
    with convert_runtime_to_click_error():
        ctx.obj.bake()


@adaux.command()
@click.pass_context
@click.argument("auxcon_file")
def pre_commit_bake(ctx: click.Context, auxcon_file: str) -> None:
    assert "auxilium." in auxcon_file
    ctx.obj.bake()


gitlab_token_option = click.option(
    "-t",
    "--token",
    prompt=os.environ.get("GITLAB_API_TOKEN", "") == "",
    help="Gitlab Access Token with API Scope.",
    default="env:GITLAB_API_TOKEN",
)


@adaux.command()
@click.pass_context
@gitlab_token_option
def gitlab(ctx: click.Context, token: str) -> None:
    r"""
    Sets various settings on the remote gitlab repositroy.
    """
    token = _get_token_from_env(token)
    with convert_runtime_to_click_error():
        ctx.obj.gitlab(token)


@adaux.command()
@click.pass_context
@gitlab_token_option
@click.option(
    "-w",
    "--watch",
    default=False,
    is_flag=True,
    help="Check the pipeline status all 30 seconds.",
)
@click.option(
    "-a",
    "--show-success",
    is_flag=True,
    default=False,
    help="Show successful jobs.",
)
def pipeline(ctx: click.Context, token: str, watch: bool, show_success: bool) -> None:
    r"""
    Shows the most recend pipeline on the cli.
    """
    token = _get_token_from_env(token)
    with convert_runtime_to_click_error():
        while True:
            done, _ = ctx.obj.pipeline(token, show_success)
            if done or not watch:
                break
            time.sleep(30)


@adaux.command()
@click.pass_context
@click.option(
    "-M",
    "--major",
    is_flag=True,
    default=False,
    help="major tick",
)
@click.option(
    "-m",
    "--minor",
    is_flag=True,
    default=False,
    help="minor tick",
)
@click.option(
    "-c",
    "--commit",
    is_flag=True,
    default=False,
    help="commit with release message",
)
@click.argument("release_message", nargs=-1)
def tick(
    ctx: click.Context, release_message: str, major: bool, minor: bool, commit: bool
) -> None:
    r"""
    Tick the version and add the release note.
    """
    with convert_runtime_to_click_error():
        ctx.obj.tick(" ".join(release_message), major, minor, commit)


@adaux.command()
@click.pass_context
@gitlab_token_option
@click.option(
    "-w",
    "--watch",
    default=False,
    is_flag=True,
    help="Check the release status all 30 seconds.",
)
@click.option(
    "-p",
    "--pipeline-check",
    default=False,
    is_flag=True,
    help="Wait for successful pipeline status before executing release.",
)
@click.option(
    "-r",
    "--rerelease",
    default=False,
    is_flag=True,
    help="Allow the MR to have the same name as past closed MR.",
)
def release(  # pylint: disable=too-many-arguments
    ctx: click.Context, token: str, watch: bool, pipeline_check: bool, rerelease: bool
) -> None:
    r"""
    Create and display release merge request.
    """
    token = _get_token_from_env(token)
    with convert_runtime_to_click_error():
        success = not pipeline_check
        if pipeline_check:
            while True:
                done, success = ctx.obj.pipeline(token, show_success=False)
                if done or not watch:
                    break
                time.sleep(30)

        # will be skipped if pipeline is checked and failed
        while success:
            done, _ = ctx.obj.release(token, rerelease)
            if done or not watch:
                break
            time.sleep(30)


@adaux.command()
@click.pass_context
@click.option("-f", "--force", is_flag=True, default=False)
@click.argument("src", type=click.Path(exists=True), default=Path("auxilium.cfg"))
@click.argument("dest", type=Path, default=Path("auxilium.yml"))
def convert(ctx: click.Context, src: Path, dest: Path, force: bool) -> None:
    r"""
    Convert auxilium file into different format, e.g. cfg -> yml.
    """
    src = Path(src)
    with convert_runtime_to_click_error():
        ctx.obj.convert(src, dest, force)


def fwd_all_inputs(fct: tp.Any) -> tp.Any:
    return adaux.command(context_settings={"ignore_unknown_options": True})(
        click.pass_context(click.argument("args", nargs=-1)(fct))
    )


@adaux.command()
@click.pass_context
@click.argument("trigger_str", nargs=1)
@click.option("-d", "--dry", is_flag=True, default=False)
def ci(ctx: click.Context, trigger_str: tp.List[str], dry: bool) -> None:
    """
    Allows running the CI locally.
    """
    with convert_runtime_to_click_error():
        return_code = ctx.obj.ci(trigger_str, dry=dry)
    ctx.exit(return_code)


@adaux.command()
@click.pass_context
def cov(ctx: click.Context, open_html: bool) -> None:
    """
    Creates the coverage html report.
    """
    with convert_runtime_to_click_error():
        ctx.obj.cov(open_html)


@fwd_all_inputs
def dcp(ctx: click.Context, args: tp.List[str]) -> None:
    """
    Shortcut for docker compose with corresponding compose file.
    """
    with convert_runtime_to_click_error():
        ctx.obj.dcp(*args)


@adaux.command(context_settings={"ignore_unknown_options": True})
@click.pass_context
@click.argument("composition")
@click.argument("args", nargs=-1)
def comp(ctx: click.Context, composition: str, args: tp.List[str]) -> None:
    """
    Shortcut for specific compositions shell file: x-compose.sh
    """
    with convert_runtime_to_click_error():
        ctx.obj.comp(composition, *args)


@adaux.command()
@click.pass_context
@click.argument("payload_names", nargs=-1)
@click.option(
    "-f", "--force", is_flag=True, default=False, help="runs payload even if up to date"
)
def run(ctx: click.Context, payload_names: tp.Tuple[str, ...], force: bool) -> None:
    """
    Run a specified payload. Use 'ls' to list all available payloads.
    """
    with convert_runtime_to_click_error():
        ctx.obj.run(*payload_names, force=force)


@adaux.command()
@click.pass_context
@click.option("-h", "--open-html", is_flag=True, default=False)
def docs(ctx: click.Context, open_html: bool) -> None:
    """
    Creates the docs.
    """
    with convert_runtime_to_click_error():
        ctx.obj.docs(open_html)


@fwd_all_inputs
def mp(ctx: click.Context, args: tp.List[str]) -> None:
    """
    Shows the first lines of the mypy pre-commit hook.
    """
    with convert_runtime_to_click_error():
        ctx.obj.mp(*args)


@fwd_all_inputs
def pipi(ctx: click.Context, args: tp.List[str]) -> None:
    """
    Runs pip install with editable=strict option.
    """
    with convert_runtime_to_click_error():
        ctx.obj.pipi(*args)


@fwd_all_inputs
def pl(ctx: click.Context, args: tp.List[str]) -> None:
    """
    Shows the first lines of the pylint pre-commit hook.
    """
    with convert_runtime_to_click_error():
        ctx.obj.pl(*args)


@fwd_all_inputs
def pra(ctx: click.Context, args: tp.List[str]) -> None:
    """
    Runs all pre-commit hooks, or a specific one if supplied.
    """
    with convert_runtime_to_click_error():
        ctx.obj.pra(*args)


@adaux.command()
@click.pass_context
@click.option("-z", "--zipped", is_flag=True, default=False)
def sdist(ctx: click.Context, zipped: bool) -> None:
    """
    Builds the release package.
    """
    with convert_runtime_to_click_error():
        ctx.obj.sdist(zipped)


@adaux.command()
@click.pass_context
@click.option("-c", "--close", default=None)
@click.option("-i", "--gitignore", is_flag=True, default=False)
@click.argument("args", nargs=-1)
def todo(
    ctx: click.Context,
    args: tp.List[str],
    close: tp.Optional[str] = None,
    gitignore: bool = False,
) -> None:
    """
    Read and write todos.
    """
    with convert_runtime_to_click_error():
        new = " ".join(args) if args else None
        ctx.obj.todo_and_note("todo", new, close, gitignore)


@adaux.command()
@click.pass_context
@click.option("-c", "--close", default=None)
@click.option("-i", "--gitignore", is_flag=True, default=False)
@click.argument("args", nargs=-1)
def note(
    ctx: click.Context,
    args: tp.List[str],
    close: tp.Optional[str] = None,
    gitignore: bool = False,
) -> None:
    """
    Read and write notes.
    """
    with convert_runtime_to_click_error():
        new = " ".join(args) if args else None
        ctx.obj.todo_and_note("note", new, close, gitignore)


def _get_token_from_env(token: str) -> str:
    default = os.environ.get("GITLAB_API_TOKEN", "")
    if default == "":
        if token == "env:GITLAB_API_TOKEN":
            raise click.UsageError("GITLAB_API_TOKEN is not set!")
        click.secho(
            f"if you want to avoid re-entering, run: ' export GITLAB_API_TOKEN={token}'",
            fg="yellow",
        )

    if token == "env:GITLAB_API_TOKEN":
        token = default
    return token


@contextlib.contextmanager
def convert_runtime_to_click_error() -> tp.Iterator[None]:
    try:
        yield
    except RuntimeError as err:
        raise click.UsageError(err.args[0])


def raise_if_not_init(ctx: click.Context) -> None:
    if ctx.invoked_subcommand not in ["init"]:
        raise click.UsageError(
            f"{ctx.obj.auxcon_file} does not exists! use 'adaux init' to create one."
        )


def raise_if_init_and_not_force(ctx: click.Context) -> None:
    if ctx.invoked_subcommand in ["init"]:
        if all(x not in sys.argv for x in ["-f", "--force"]):
            raise click.UsageError(
                f"{ctx.obj.auxcon_file} already exists, Use 'adaux update' or -f to overwrite."
            )
