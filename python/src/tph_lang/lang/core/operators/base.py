from __future__ import annotations

from typing import Any
from abc import ABC, abstractmethod


class Operator(ABC):
    @abstractmethod
    def compute(self, *args: Any, **kwargs: Any) -> Any: ...
