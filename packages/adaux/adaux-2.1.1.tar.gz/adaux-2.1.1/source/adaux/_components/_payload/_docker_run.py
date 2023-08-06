# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import dataclasses as dc
import typing as tp

from ._docker import DockerPayload
from ._docker_executors import DockerRun

__all__ = ["DockerRunPayload"]


@dc.dataclass
class DockerRunPayload(DockerPayload):
    flavor: tp.ClassVar[str] = "docker_run"

    def create_executor(self, parents: tp.Any) -> tp.Any:
        # pylint: disable=attribute-defined-outside-init
        return DockerRun(
            slug=self.auxh.project.slug, services=self.param.services, parents=parents
        )
