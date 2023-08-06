# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import dataclasses as dc
import typing as tp

from ..._proto_namespace import _ProtoNamespace

__all__ = ["Payload"]


@dc.dataclass
class Payload:
    flavor: tp.ClassVar[str]
    name: str
    auxh: _ProtoNamespace

    def run(self, force: bool) -> None:  # pylint: disable=unused-argument
        raise NotImplementedError()

    def is_up_to_date(self) -> bool:
        return False

    def hydrate(self, deps: tp.Tuple["Payload", ...] = tuple()) -> None:
        pass
