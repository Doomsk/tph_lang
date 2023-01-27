from abc import ABC, abstractmethod
from copy import deepcopy
from tph_lang.core import DIR_LIST
from tph_lang.core.operations import (
    directions,
    scopes
)


class ArrayClass:
    def __init__(self, name):
        self.name = name
        self.array = []

    def append(self, value):
        self.array.append(value)

    def extend(self, value):
        self.array.extend(value)

    def set(self, value):
        self.array = value if isinstance(value, list) else [value]

    def pop(self, value=0):
        return self.array.pop(value if value < len(self.array) else 0)

    def clean(self):
        self.array = []

    def copy(self):
        return deepcopy(self.array)

    def swap(self, array):
        self.array, array = deepcopy(array), deepcopy(self.array)

    def __len__(self):
        return len(self.array)

    def __iter__(self):
        yield from self.array

    def __getitem__(self, item):
        return self.array[item]

    def __repr__(self):
        return f"{self.array}"


class ArrayGroup:
    def __init__(
            self,
            cur_pos: tuple,
            cur_dir="right",
            scope="main",
            endline=False,
            marginal=False
    ):
        self._scope = self.check_scope(scope)
        self._endline = self.check_endline(endline)
        self._cur_pos = self.check_pos(cur_pos)
        self._cur_dir = self.check_dir(cur_dir)
        self.marginal = marginal
        self._main_array = ArrayClass("main")
        self._lhs_array = ArrayClass("lhs")
        self._rhs_array = ArrayClass("rhs")
        self.from_scope = {
            "main": self._main_array,
            "lhs": self._lhs_array,
            "rhs": self._rhs_array
        }

    @staticmethod
    def check_pos(data):
        if isinstance(data, tuple):
            if len(data) == 2 and all([isinstance(k, int) for k in data]):
                return data
        raise ValueError(f"invalid position given '{data}'.")

    @staticmethod
    def check_dir(data):
        if data in directions or data in DIR_LIST:
            return data
        raise ValueError(f"invalid direction given '{data}'.")

    @staticmethod
    def check_scope(data):
        if data in scopes:
            return data
        raise ValueError(f"invalid scope given '{data}'.")

    @staticmethod
    def check_endline(data):
        if isinstance(data, bool):
            return data
        raise ValueError(f"invalid endline given '{data}'.")

    @property
    def main(self):
        return self._main_array

    @main.setter
    def main(self, data):
        if data is not None:
            self._main_array.set(deepcopy(data))

    @property
    def lhs(self):
        return self._lhs_array

    @lhs.setter
    def lhs(self, data):
        if data is not None:
            self._lhs_array.set(deepcopy(data))

    @property
    def rhs(self):
        return self._rhs_array

    @rhs.setter
    def rhs(self, data):
        if data is not None:
            self._rhs_array.set(deepcopy(data))

    def __getitem__(self, item):
        if item == "main":
            return self.main
        if item == "lhs":
            return self.lhs
        if item == "rhs":
            return self.rhs
        raise ValueError(f"array group cannot resolve '{item}'.")

    @property
    def endline(self):
        return self._endline

    @endline.setter
    def endline(self, data):
        if isinstance(data, bool):
            self._endline = data

    @property
    def cur_pos(self):
        return self._cur_pos

    @cur_pos.setter
    def cur_pos(self, data):
        if isinstance(data, tuple):
            self._cur_pos = data

    @property
    def cur_dir(self):
        return self._cur_dir

    @cur_dir.setter
    def cur_dir(self, data):
        if data in ["right", "left", "up", "down"]:
            self._cur_dir = data

    def flush(self):
        return deepcopy(self.cur_pos), deepcopy(self.cur_dir)


class AllOpers(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class OperType1(AllOpers):
    """
    Operators that may require only one entry argument
    and one output for destination
    """
    pass


class OperType2(AllOpers):
    """
    Operators that may require only one entry argument
    and two outputs for destination
    """


class OperType3(AllOpers):
    """
    Operators that may require two entry arguments
    and one output for destination
    """
    pass


class OperType4(AllOpers):
    """
    Operators that may require two entry arguments
    and two output for destination
    """


class OperType5(AllOpers):
    """
    Operators that may require three entry arguments
    and one output destination
    """
