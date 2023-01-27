import re
from tph_lang.core import (
    opers_dict,
    int_literal,
    str_literal,
    OperS,
    DirS,
    DIR_LIST,
    LiteralS,
)


class Symbol:
    def __init__(self, value, prev_char=None):
        self.value, self.name = self.check_symbols(value) or self.check_lit(value, prev_char)

    @staticmethod
    def check_symbols(data):
        if data in opers_dict.keys():
            print(f'symbol {data} {opers_dict[data]}')
            return data, opers_dict[data]
        return False

    @staticmethod
    def check_lit(data, prev_char=None):
        if prev_char is None:
            if re.findall(int_literal[0], data):
                return data, LiteralS.DIGIT
        elif prev_char == OperS.QUOTE:
            return data, LiteralS.STR
        return False

    def isnumeric(self):
        pass

    def __hash__(self):
        return sum([ord(k) * ord(self.value or " ") for k in f"{self.name}"])

    def __eq__(self, value):
        return self.__hash__() == value.__hash__()

    def __contains__(self, item):
        return item in self.name

    def __bool__(self):
        return True if self.value is not None else False

    def __repr__(self):
        return str(self.value)


class AST:
    def __init__(self, name, pos, value_dir, value=None, lhs=None, rhs=None):
        self.name = name
        self.pos = pos
        if value_dir in DIR_LIST:
            self.dir = value_dir
            self.main = value
            self.lhs = lhs
            self.rhs = rhs
        else:
            raise ValueError(f"wrong value dir '{value_dir}'.")

    def has_main(self):
        return True if self.main else False

    def has_lhs(self):
        return True if self.lhs else False

    def has_rhs(self):
        return True if self.rhs else False

    def __repr__(self):
        res = f"AST(name={self.name}, pos={self.pos}, dir={self.dir},"
        if self.main is not None:
            res += f" MAIN=[{self.main}]"
        if self.lhs is not None:
            res += f", LHS=[{self.lhs}]"
        if self.rhs is not None:
            res += f", RHS=[{self.rhs}]"
        res += ")"
        return res
