import re
from copy import deepcopy
from tph_lang.core.operations import (
    # general_symbols_tuple,
    general_symbols_dict as table,
    name_std_dict,
    literals_tuple,
    directions,
    scopes
)


class Symbol:
    # table = general_symbols_tuple

    def __init__(self, value):
        self.value, self.name = self.check_lit(value) or self.check_symbols(value)

    def check_symbols(self, data):
        if data in table.keys():
            value = table[data]
            return name_std_dict[value], value
        # for k in self.table:
        #     if data == k[0]:
        #         return name_std_dict[k[1]], k[1]
        raise ValueError(f"cannot find symbol {data}.")

    @staticmethod
    def check_lit(data):
        if data is not None:
            return (data, literals_tuple[0][1]) if data.isnumeric() else False
        return ''

    def isnumeric(self):
        return True if re.findall(literals_tuple[0][0], self.value) else False

    def __hash__(self):
        return sum([ord(k) * ord(self.value or " ") for k in f"{self.name}"])

    def __eq__(self, value):
        return self.__hash__() == value.__hash__()

    def __bool__(self):
        return True if self.value is not None else False

    def __repr__(self):
        return str(self.value)


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
        self.main_array = ArrayClass("main")
        self.lhs_array = ArrayClass("lhs")
        self.rhs_array = ArrayClass("rhs")
        self.from_scope = {
            "main": self.main_array,
            "lhs": self.lhs_array,
            "rhs": self.rhs_array
        }

    @staticmethod
    def check_pos(data):
        if isinstance(data, tuple):
            if len(data) == 2 and all([isinstance(k, int) for k in data]):
                return data
        raise ValueError(f"invalid position given '{data}'.")

    @staticmethod
    def check_dir(data):
        if data in directions:
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
        return self.main_array

    @main.setter
    def main(self, data):
        # if isinstance(data, list):
        #     self.main_array.set(deepcopy(data))
        # else:
        #     self.main_array.set(data)
        self.main_array.set(data)

    @property
    def lhs(self):
        return self.lhs_array

    @lhs.setter
    def lhs(self, data):
        self.lhs_array.set(data)

    @property
    def rhs(self):
        return self.rhs_array

    @rhs.setter
    def rhs(self, data):
        self.rhs_array.set(data)

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
