# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import dataclasses as dc
import types
import typing as tp

from ..._proto_namespace import _ProtoNamespace
from ._base import Payload

__all__ = ["PythonPayload"]


@dc.dataclass
class PythonPayload(Payload):
    flavor: tp.ClassVar[str] = "python"
    fct: tp.Callable[
        [
            tp.Dict[str, tp.Any],
        ],
        bool,
    ]
    param: _ProtoNamespace = dc.field(default_factory=_ProtoNamespace)

    def run(self, force: bool = False) -> None:
        if hasattr(self, "_deps"):
            self.fct(self.auxh, self._deps, **self.param)  # type: ignore
        else:
            self.fct(self.auxh, **self.param)

    @classmethod
    def import_function(
        cls, name: str, custom_ppyload: tp.Optional[types.ModuleType]
    ) -> tp.Callable[[tp.Dict[str, tp.Any],], bool]:
        # pylint: disable=import-outside-toplevel
        from ...src.payload.python import functions as fallback

        fname = name.replace("-", "_")
        try:
            return getattr(custom_ppyload, fname)  # type: ignore
        except AttributeError:
            return getattr(fallback, fname)  # type: ignore

    def hydrate(self, deps: tp.Tuple["Payload", ...] = tuple()) -> None:
        if hasattr(self, "is_hydrated"):
            return
        # pylint: disable=attribute-defined-outside-init
        self.is_hydrated = True
        if deps:
            self._deps = deps
