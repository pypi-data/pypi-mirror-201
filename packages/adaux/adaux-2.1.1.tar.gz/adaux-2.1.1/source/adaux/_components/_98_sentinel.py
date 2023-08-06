# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import contextlib
import typing as tp

from .._logging import logger
from .._proto_namespace import _ProtoNamespace
from ._00_extra_level import ExtraLevel
from ._02_base import BaseComponent


class SentinelMixin(BaseComponent):
    def __init__(self, *args: tp.Any, **kwgs: tp.Any) -> None:
        super().__init__(*args, **kwgs)
        self._auxcon_entered = False

    def bake(self) -> None:
        with self.extra():
            super().bake()
            self.writeout()

    def formatted(self) -> None:
        # idempotent guard
        if hasattr(self, "auxf"):
            return
        super().formatted()

    def defaulted(self) -> None:
        # idempotent guard
        if hasattr(self, "auxd"):
            return
        super().defaulted()

    def enriched(self) -> None:
        # idempotent guard
        if hasattr(self, "auxe"):
            return
        super().enriched()

    def hydrated(self) -> None:
        # idempotent guard
        if hasattr(self, "auxh"):
            return
        super().hydrated()

    @contextlib.contextmanager
    def extra(
        self, level: ExtraLevel = ExtraLevel.ENRICHED
    ) -> tp.Iterator[_ProtoNamespace]:
        logger.info("enabled %s", level)
        if level == ExtraLevel.TEMPLATED:
            self.templated()
            self.formatted()
            yield self.auxf
            del self.auxf
        elif level == ExtraLevel.DEMODATA:
            self.templated()
            self.demodata()
            self.formatted()
            yield self.auxf
            del self.auxf
        if level == ExtraLevel.FORMATTED:
            self.formatted()
            yield self.auxf
            del self.auxf
        elif level == ExtraLevel.DEFAULTED:
            self.formatted()
            self.defaulted()
            yield self.auxd
            del self.auxd
            del self.auxf
        elif level == ExtraLevel.ENRICHED:
            self.formatted()
            self.defaulted()
            self.enriched()
            yield self.auxe
            del self.auxe
            del self.auxd
            del self.auxf
        elif level == ExtraLevel.HYDRATED:
            self.formatted()
            self.defaulted()
            self.enriched()
            self.hydrated()
            yield self.auxh
            del self.auxh
            del self.auxe
            del self.auxd
            del self.auxf
        logger.info("disabled %s", level)
