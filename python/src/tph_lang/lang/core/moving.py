from __future__ import annotations

from enum import Enum, auto
from typing import Any

from tph_lang.lang.core.parser import Code


class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()
    DOWN = auto()
    UP = auto()


class Points:
    def __init__(self):
        pass

    def _gen_points(self, code: Code) -> Any:
        pass

    def next(self, direction: Direction) -> Any:
        pass

    def peek(self, direction: Direction) -> Any:
        pass

    def has_lhs(self) -> bool:
        pass

    def has_rhs(self) -> bool:
        pass


class UnitPosition:
    pass


class CodeMap:
    def __init__(self, code: Code):
        pass

    def gen_points_map(self, code: Code):
        points = []
        for n, k in enumerate(code):
            for m, q in enumerate(k):
                sub_points = []
                if q not in ["", "\n", "\t", " "]:
                    sub_points.append(m)


