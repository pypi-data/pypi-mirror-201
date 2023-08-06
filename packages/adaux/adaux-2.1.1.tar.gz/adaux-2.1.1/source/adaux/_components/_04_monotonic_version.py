# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
from pathlib import Path

from .._util import LazyVersionStr
from ._02_base import BaseComponent


class MonotonicVersionMixin(BaseComponent):
    def bake(self) -> None:
        super().bake()
        self._raise_if_iv_older_than_luv()

    @property
    def _luv_file(self) -> Path:
        res: Path = self.target / "auxilium" / "last-used-version.txt"
        return res

    def _raise_if_iv_older_than_luv(self) -> None:
        # iv :installed version
        # luv : last used version
        inst_vers = str(LazyVersionStr())
        if self._luv_file.exists():
            with self._luv_file.open("r") as f:
                lu_vers = f.readline().strip()
        else:
            lu_vers = inst_vers

        iv_split = list(map(int, inst_vers.split(".")))
        luv_split = list(map(int, lu_vers.split(".")))
        if iv_split < luv_split:
            raise RuntimeError(
                f"""
                you are trying to run aux bake with version adaux=={inst_vers},
                but this project has been baked with a newer version {lu_vers}.
                Consider upgrading:  pip install adaux --upgrade
                """
            )

    def writeout(self) -> None:
        super().writeout()
        self._luv_file.parent.mkdir(parents=True, exist_ok=True)
        with self._luv_file.open("w") as f:
            f.write(f"{LazyVersionStr()}\n")
