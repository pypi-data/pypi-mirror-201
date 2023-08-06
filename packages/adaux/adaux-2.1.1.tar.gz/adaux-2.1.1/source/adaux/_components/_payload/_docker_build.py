# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import dataclasses as dc
import typing as tp

from ._docker import DockerPayload

__all__ = ["DockerBuildPayload"]


from ._docker_executors import DockerBuild


@dc.dataclass
class DockerBuildPayload(DockerPayload):
    flavor: tp.ClassVar[str] = "docker_build"

    def create_executor(self, parents: tp.Any) -> tp.Any:
        return DockerBuild(
            slug=self.auxh.project.slug,
            service=self.param.service_name,
            image_name=self.param.image_name,
            branch_match=[],
            base_match=[],
            parents=parents,
            files=[f"devops/docker/{self.param.service_name}.dockerfile"],
        )

    def is_up_to_date(self) -> bool:
        return self.executor.is_up_to_date()  # type: ignore
