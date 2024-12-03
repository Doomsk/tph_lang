from __future__ import annotations

from typing import Any, Iterator


class Code:
    def __init__(self, file_name: str):
        with open(file_name, "r") as file:
            self.data = file.readlines()

    def _factor_code(self) -> None:
        self.data = []

    def __iter__(self) -> Iterator:
        yield from self.data
