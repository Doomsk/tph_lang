from __future__ import annotations

from typing import Any

from tph_lang.lang.core.operators.operators import (
    Right,
    EndProgram,
)


class Evaluator:
    @classmethod
    def code_walk(cls, code: str) -> Any:
        pass

    @classmethod
    def run(cls, code: str) -> Any:
        pass
