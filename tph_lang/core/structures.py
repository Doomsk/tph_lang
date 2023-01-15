import re
from tph_lang.core.operations import (
    general_symbols_tuple,
    name_std_dict,
    literals_tuple
)


class Symbol:
    table = general_symbols_tuple

    def __init__(self, value):
        self.value, self.name = self.check_lit(value) or self.check_symbols(value)

    def check_symbols(self, data):
        for k in self.table:
            if data == k[0]:
                return name_std_dict[k[1]], k[1]
        raise ValueError(f"cannot find symbol {data}.")

    @staticmethod
    def check_lit(data):
        return (data, literals_tuple[0][1]) if data.isnumeric() else False

    def isnumeric(self):
        return True if re.findall(literals_tuple[0][0], self.value) else False

    def __hash__(self):
        return sum([ord(k) * ord(self.value) for k in f"{self.name}"])

    def __eq__(self, value):
        return self.__hash__() == value.__hash__()

    def __repr__(self):
        return self.value
