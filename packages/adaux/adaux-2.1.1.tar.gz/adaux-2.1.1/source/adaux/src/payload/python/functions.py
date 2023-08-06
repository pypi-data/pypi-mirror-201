# pylint: disable=relative-beyond-top-level
import os
import re
import typing as tp

from ...._components._payload._docker_executors import subprocess_run
from ...._components._payload._docker_executors import tag_image
from ...._components._payload._docker_executors import upload_to_remote
from ...._proto_namespace import _ProtoNamespace


def check_release_notes(aux: _ProtoNamespace) -> None:
    release_notes = aux.project.release_notes
    version = aux.project.version
    # check that version has a note
    if version not in release_notes:
        raise RuntimeError(f"version {version} is not in release notes, please add!")
    # check that version was not already released
    out = subprocess_run(
        ["git", "ls-remote", "--tags"], check=True, capture_output=True
    )
    already_released = list(re.findall(r"tags/([\d.]+)\n", out.stdout.decode()))
    if version in already_released:
        raise RuntimeError(
            f"version {version} was already released and cannot be released again!"
        )

    print(f"version {version} has description '{release_notes[version]}'")


def gitlab_release(aux: _ProtoNamespace) -> None:
    release_notes = aux.project.release_notes
    version = aux.project.version
    description = release_notes[version]
    os.environ["RELEASE_TAG"] = version
    os.environ["RELEASE_DESCRIPTION"] = description
    payload = aux.payload.lookup["gitlab-release-run"]
    payload.run()


def tag(
    aux: _ProtoNamespace,  # pylint: disable=unused-argument
    deps: tp.Any,
    tag: str,  # pylint: disable=redefined-outer-name
) -> None:
    if len(deps) != 1:
        raise RuntimeError(
            f"tag job for {tag} should have exactly 1 dependency, not {len(deps)}!"
        )
    tag = tag.format(version=aux.project.version)
    local_tag, release_tag = deps[0].executor.tag_and_upload(tag)
    print("uploaded", local_tag)
    print("   -> to", release_tag)


def img_dockerhub(
    aux: _ProtoNamespace,
    deps: tp.Any,
    release_tag: str,
) -> None:
    if len(deps) != 1:
        raise RuntimeError(
            f"img-dockerhub job for {release_tag} should have exactly 1 dependency, not {len(deps)}!"
        )
    release_tag = release_tag.format(
        version=aux.project.version, ci_adaux_image=aux.versions.ci_adaux_image
    )
    local_tag = deps[0].executor.pull_if_not_existent()
    tag_image(local_tag, release_tag)
    subprocess_run(
        [
            "docker",
            "login",
            "-u",
            os.environ["DOCKERHUB_USERNAME"],
            "-p",
            os.environ["DOCKERHUB_PASSWORD"],
            "docker.io",
        ]
    )
    upload_to_remote(local_tag, release_tag)
    subprocess_run(["docker", "logout", "docker.io"])
    print("uploaded", local_tag)
    print("   -> to", release_tag)
