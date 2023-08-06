# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
from ._15_pytest import PytestMixin


class CoverageMixin(PytestMixin):
    def templated(self) -> None:
        super().templated()
        self.auxcon.dependencies.test.append(self.versions.pytest_cov)
