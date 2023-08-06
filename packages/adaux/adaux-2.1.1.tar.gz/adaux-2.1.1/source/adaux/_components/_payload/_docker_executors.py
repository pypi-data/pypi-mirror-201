# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import dataclasses as dc
import functools
import hashlib
import os
import re
import subprocess
import sys
import typing as tp

import requests

from ..._logging import logger


@dc.dataclass(frozen=True)
class DockerShared:
    slug: str
    parents: tp.Tuple["DockerShared", ...] = tuple()

    # Run local registry:
    # docker run -d -p 5000:5000 --name registry registry:2
    # docker container stop registry && docker container rm -v registry
    # export CI_REGISTRY=localhost:5000
    @property
    def registry_host(self) -> str:
        return os.environ["CI_REGISTRY"]

    def remote_exists(self) -> bool:
        return "CI_REGISTRY" in os.environ

    @property
    def build_deps(self) -> tp.Iterator["DockerBuildMixin"]:
        for parent in self.parents:
            if isinstance(parent, DockerBuildMixin):
                yield parent

    def script(self) -> None:
        # get dependencies
        for job in self.build_deps:
            local_tag = job.local_tag
            if not exists_locally(local_tag):
                if self.remote_exists():
                    remote_tag = job.remote_tag
                    if not exists_locally(remote_tag):
                        cmd = ["docker", "pull", remote_tag]
                        subprocess_run(cmd, check=True, capture_output=True)
                        logger.info("pulled '%s'", remote_tag)

                    tag_image(remote_tag, job.local_tag)

            # I tag every time as it allows different dependencies to
            # map to the same service name without raising issues
            # (useful for local development)
            tag_image(job.local_tag, job.use_tag)

    def _get_tag_parts(self) -> tp.Iterator[tp.Union[bytes, str]]:
        for job in self.build_deps:
            yield job.tag


@dc.dataclass(frozen=True)
class _DockerBuildMixinState:
    service: str
    image_name: str


@dc.dataclass(frozen=True)
class DockerBuildMixin(DockerShared, _DockerBuildMixinState):
    images: tp.List[str] = dc.field(default_factory=list)
    files: tp.List[str] = dc.field(default_factory=list)

    def script(self) -> None:
        super().script()
        local_tag = self.local_tag
        if self.remote_exists():
            remote_tag = self.remote_tag

            check_and_pull_if_not_existent(remote_tag, self.service, local_tag)
            # download other images which are not a direct dependency (cross-repo)
            for image_tag in self.images:
                image_remote_tag = (
                    f"{self.registry_host}/{self._remove_namespace_local(image_tag)}"
                )
                check_and_pull_if_not_existent(image_remote_tag, image_tag)

        # build
        cmd = [
            "docker",
            "--log-level",
            "ERROR",
            "compose",
            "-p",
            self.slug,
            "-f",
            "devops/docker/compose.yml",
            "build",
            self.service,
        ]
        subprocess_run(cmd, check=True)

        # upload
        tag_image(self.use_tag, local_tag)
        if self.remote_exists():
            upload_to_remote(local_tag, remote_tag)
            logger.info("uploaded %s to %s", local_tag, remote_tag)

    @functools.cached_property
    def tag(self) -> str:
        hasher = hashlib.md5()

        for part in self._get_tag_parts():
            if isinstance(part, str):
                hasher.update(part.encode("utf8"))
            else:
                hasher.update(part)

        tag = hasher.hexdigest()[:16]
        return f"aux-{tag}"

    def _get_tag_parts(self) -> tp.Iterator[tp.Union[bytes, str]]:
        yield from super()._get_tag_parts()
        for file in self.files:
            with open(file, "rb") as f:
                yield f.read()

        # we assume the image tag is not moving (i.e. no latest)
        yield from self.images

    @functools.cached_property
    def remote_tag(self) -> str:
        return f"{self.registry_host}/{self.local_tag}"

    @functools.cached_property
    def local_tag(self) -> str:
        image = self.get_image_name()
        return f"{image}:{self.tag}"

    @functools.cached_property
    def use_tag(self) -> str:
        return self.image_name.lower()

    def get_image_name(self) -> str:
        if "CI_PROJECT_NAMESPACE" in os.environ:
            group = os.environ["CI_PROJECT_NAMESPACE"]
            repo = os.environ["CI_PROJECT_NAME"]
            return f"{group}/{repo}/{self.use_tag}".lower()
        return f"{self.use_tag}"

    def _docker_registry_header_and_url(
        self, image: str
    ) -> tp.Tuple[tp.Dict[str, str], str]:
        protocol = "http"
        headers = {}
        if not self.registry_host.startswith("localhost"):
            protocol = "https"
            headers["Authorization"] = f"Bearer {registry_api_token(image)}"

        # https://gitlab.com/gitlab-org/gitlab/-/issues/19470
        url = f"{protocol}://{self.registry_host}/v2"
        return headers, url

    def is_up_to_date(self) -> bool:
        if self.remote_exists():
            return self.exists_remotely()
        return exists_locally(self.local_tag)

    def _remove_namespace_local(self, image: str) -> str:
        if self.registry_host.startswith("localhost"):
            return image.rsplit("/", 1)[1]
        return image

    def exists_remotely(self) -> bool:
        headers, api_url = self._docker_registry_header_and_url(self.get_image_name())
        try:
            req = requests.get(
                api_url + f"/{self.get_image_name()}/tags/list",
                headers=headers,
                timeout=10,
            )
        except requests.ConnectionError as err:
            raise RuntimeError(
                f"are you sure the registry {self.registry_host} is reachable?\n"
                "use: docker run -d -p 5000:5000 --name registry registry:2"
            ) from err

        if req.status_code != 200:
            return False
        tags = req.json()["tags"] or []
        return self.tag in tags

    def tag_and_upload(self, tag: str) -> tp.Tuple[str, str]:
        remote_tag = self.remote_tag
        local_tag = self.local_tag
        assert isinstance(self, DockerBuild)
        check_and_pull_if_not_existent(remote_tag, local_tag)
        release_tag = remote_tag.replace(self.tag, tag)
        upload_to_remote(local_tag, release_tag)
        return local_tag, release_tag

    def pull_if_not_existent(self) -> str:
        remote_tag = self.remote_tag
        local_tag = self.local_tag
        assert isinstance(self, DockerBuild)
        check_and_pull_if_not_existent(remote_tag, local_tag)
        return local_tag


@dc.dataclass(frozen=True)
class _DockerBuildBranchMatchMixinState(_DockerBuildMixinState):
    branch_match: tp.List[tp.Tuple[str, str, str, tp.List[str], tp.Optional[str]]]


@dc.dataclass(frozen=True)
class MatchCommonImpl:
    @classmethod
    def _get_git_branch(cls) -> str:
        branch = os.environ.get("CI_COMMIT_BRANCH", "") + os.environ.get(
            "CI_MERGE_REQUEST_SOURCE_BRANCH_NAME", ""
        )
        if not branch:
            # we are running it locally, and try to get it from git
            proc = subprocess.run(
                ["git", "branch", "--show-current"], check=False, capture_output=True
            )
            if proc.returncode == 0:
                branch = proc.stdout.decode("utf-8").strip()

        assert branch
        return branch


@dc.dataclass(frozen=True)
class DockerBuildBranchMatchMixin(
    MatchCommonImpl, DockerBuildMixin, _DockerBuildBranchMatchMixinState
):
    def _get_tag_parts(self) -> tp.Iterator[tp.Union[bytes, str]]:
        yield from super()._get_tag_parts()

        branch = self._get_git_branch()

        for pkg, var, url, skip, fallback in self.branch_match:
            if branch in skip:
                logger.info("skipping matching branch '%s' for '%s'", branch, pkg)
                continue
            secret = re.search(r"\$(\w+)@", url).group(1)  # type: ignore
            url = url.replace(f"${secret}", os.environ[secret])
            # figure out if matching branch exists

            try_branches = [(branch, "matching")]
            if fallback:
                try_branches.append((fallback, "fallback"))

            for branch, reason in try_branches:
                exists, sha = self._matching_branch_exist(url, branch)
                if exists:
                    logger.info("found %s branch '%s' for '%s'", reason, branch, pkg)
                    yield sha
                    os.environ[var] = f"{pkg}@git+{url}@{branch}"
                    break

    @classmethod
    def _matching_branch_exist(cls, url: str, branch: str) -> tp.Tuple[bool, str]:
        cmd = f"git ls-remote {url} {branch}".split(" ")
        res = subprocess_run(cmd, check=False, capture_output=True)
        if res.returncode != 0:
            raise RuntimeError(res.stderr.decode("utf8"))
        parts = res.stdout.decode("utf8").split()
        if parts:
            sha, refs = parts
            assert branch in refs
            return True, sha
        return False, ""


@dc.dataclass(frozen=True)
class _DockerBuildBaseMatchMixinState(_DockerBuildMixinState):
    base_match: tp.List[tp.Tuple[str, str, tp.List[str], str, str]]


@dc.dataclass(frozen=True)
class DockerBuildBaseMatchMixin(
    MatchCommonImpl, DockerBuildMixin, _DockerBuildBaseMatchMixinState
):
    def _get_tag_parts(self) -> tp.Iterator[tp.Union[bytes, str]]:
        yield from super()._get_tag_parts()
        branch = self._get_git_branch()

        for image_w_ns, var, skip, fallback, default in self.base_match:
            # locally, we do not use the group and repo prefix, hence
            # it needs to be removed
            image = self._remove_namespace_local(image_w_ns)
            if branch in skip:
                logger.info(
                    "skipping matching base '%s' for '%s', using default '%s'",
                    branch,
                    image,
                    default,
                )
                self._fix_environ_and_image(image, var, default)
                yield default
                return

            try_bases = [(fallback, "fallback")]

            for tag, reason in try_bases:
                exists, sha = self._matching_base_exist(image, tag)
                if exists:
                    logger.info("found %s tag '%s' for '%s'", reason, tag, image)
                    self._fix_environ_and_image(image, var, tag)
                    yield sha
                    break
            else:
                logger.info(
                    "no matching base found for '%s', using default '%s'",
                    image,
                    default,
                )
                self._fix_environ_and_image(image, var, default)
                yield tag

    def _fix_environ_and_image(self, image: str, var: str, tag: str) -> None:
        unevaluated = f"{image}:${var}"
        os.environ[var] = tag

        for i, candidate in enumerate(self.images):
            if candidate.endswith(unevaluated):
                self.images[i] = candidate.replace(f"${var}", tag)

    def _matching_base_exist(self, image: str, tag: str) -> tp.Tuple[bool, str]:
        headers, api_url = self._docker_registry_header_and_url(image)
        try:
            headers["Accept"] = "application/vnd.docker.distribution.manifest.v2+json"
            req = requests.get(
                api_url + f"/{image}/manifests/{tag}", headers=headers, timeout=10
            )
            sha = req.json()["config"]["digest"]
            return True, sha
        except (requests.ConnectionError, KeyError):
            return False, ""


@dc.dataclass(frozen=True)
class _DockerRunMixinState:
    services: tp.List[str]


@dc.dataclass(frozen=True)
class DockerRunMixin(DockerShared, _DockerRunMixinState):
    def script(self) -> None:
        super().script()

        cmd = [
            "docker",
            "--log-level",
            "ERROR",
            "compose",
            "-p",
            self.slug,
            "-f",
            "devops/docker/compose.yml",
            "up",
            "--no-build",
            "--no-log-prefix",
            "--abort-on-container-exit",
            *self.services,
        ]
        subprocess_run(cmd, check=True)


@dc.dataclass(frozen=True)
class DockerBuild(
    DockerBuildBaseMatchMixin,
    DockerBuildBranchMatchMixin,
    _DockerBuildBaseMatchMixinState,
    _DockerBuildBranchMatchMixinState,
):
    pass


@dc.dataclass(frozen=True)
class DockerRun(DockerRunMixin, _DockerRunMixinState):
    pass


def subprocess_run(
    *args: tp.Any, **kwgs: tp.Any
) -> "subprocess.CompletedProcess[bytes]":
    sys.stdout.flush()
    try:
        # pylint: disable=subprocess-run-check
        return subprocess.run(*args, **kwgs)
    except subprocess.CalledProcessError as err:
        if err.stdout:
            print("========>> stdout")
            print(err.stdout.decode("utf-8"))
        if err.stderr:
            print("========>> stderr")
            print(err.stderr.decode("utf-8"))
        raise


# try to download for caching (or reuse if already there)
def check_and_pull_if_not_existent(
    remote_tag: str, service: str, local_tag: tp.Optional[str] = None
) -> None:
    if local_tag and exists_locally(local_tag):
        return

    if not exists_locally(remote_tag):
        cmd = ["docker", "pull", remote_tag]
        res = subprocess_run(cmd, check=False)
        if res.returncode != 0:
            return
        tag_image(remote_tag, service)
    if local_tag:
        tag_image(remote_tag, local_tag)


def upload_to_remote(
    local_tag: str, remote_tag: str, registry: tp.Optional[str] = None
) -> None:
    tag_image(local_tag, remote_tag)
    cmd = ["docker", "push", remote_tag]
    if registry:
        cmd += [registry]
    subprocess_run(cmd, check=True, capture_output=True)
    logger.info("pushed '%s'", remote_tag)


def tag_image(src_tag: str, dest_tag: str) -> None:
    cmd = ["docker", "image", "tag", src_tag, dest_tag]
    subprocess_run(cmd, check=True)
    logger.info("tagged '%s' -> '%s'", src_tag, dest_tag)


def exists_locally(local_tag: str) -> bool:
    cmd = ["docker", "image", "inspect", local_tag]
    res = subprocess_run(cmd, check=False, capture_output=True)
    return res.returncode == 0


@functools.lru_cache
def registry_api_token(image: str) -> str:
    # https://www.pimwiddershoven.nl/entry/request-an-api-bearer-token-from-gitlab-jwt-authentication-to-control-your-private-docker-registry
    # curl --user 'user:pw' 'https://gitlab.com/jwt/auth?client_id=docker&offline_token=true&service=container_registry&scope=repository:administratum/auxilium/adaux-pytest-39:pull,push'
    # curl -H 'Authorization: Bearer token' https://gitlab.com:5050/v2/administratum/auxilium/adaux-pytest-39/tags/list
    server = os.environ["CI_SERVER_URL"]
    url = f"{server}/jwt/auth?client_id=docker&offline_token=true&service=container_registry&scope=repository:{image}:pull,push"
    req = requests.get(
        url,
        auth=(os.environ["CI_REGISTRY_USER"], os.environ["CI_JOB_TOKEN"]),
        timeout=10,
    )
    return req.json()["token"]  # type: ignore
