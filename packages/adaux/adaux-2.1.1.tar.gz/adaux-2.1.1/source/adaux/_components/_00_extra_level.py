# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import enum

__all__ = ["ExtraLevel"]


class ExtraLevel(enum.Enum):
    FORMATTED = 0
    DEFAULTED = 1
    ENRICHED = 2
    HYDRATED = 3
    TEMPLATED = 4
    DEMODATA = 5
