from __future__ import annotations

from typing import Any

from tph_lang.lang.core.operators.base import Operator


class Right(Operator):
    def compute(self, *args: Any, **kwargs: Any) -> Any:
        pass


class Down(Operator):
    pass


class Left(Operator):
    pass


class Up(Operator):
    pass


class EndProgram(Operator):
    def compute(self, *args: Any, **kwargs: Any) -> Any:
        pass
