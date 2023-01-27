import re

from tph_lang.core.operations import general_symbols_dict as table, name_std_dict, literals_tuple


class AST:
    def __init__(self, name, value, pos=None):
        self.name = name
        print(f"AST value type {type(value)} {value}")
        self.value = self.build_values(value, pos)
        self.pos = pos if pos else (self.lines()[0], self.cols(self.lines()[0])[0])

    def build_values(self, data, pos):
        if self.name != "program":
            return {pos[0]: {pos[1]: Symbol(data)}}
        values = dict()
        for p in data:
            for k, v in p.main.items():
                for q, r in v.items():
                    values[k].update({q: r}) if k in values.keys() else values.update({k: {q: r}})
        return values

    def lines(self):
        return list(self.value.keys())

    def cols(self, line):
        return list(self.value[line].keys())

    def given_line(self, line):
        return list(self.value[line].keys())

    def given_col(self, col):
        lines = []
        for line, value in self.value.items():
            if col in value.keys():
                lines.append(line)
        return lines

    @staticmethod
    def get_inner(x):
        yield from x.items() if isinstance(x, dict) else x

    def __iter__(self):
        yield from map(lambda x: (x[0], self.get_inner(x[1])), self.value.items())

    def get_line(self, value, other=None):
        return self.value.get(value, other)

    def get(self, pos):
        return self.value[pos[0]][pos[1]]

    def __getitem__(self, value):
        return self.value.get(value, None)

    def __repr__(self):
        header = "AST:\n line |   pos   | cmd\n"
        body = ""
        for k, v in self:
            for n, p in enumerate(v):
                body += f" {' ' * (4 - len(str(n)))}{n}"
                body += f"  ({' ' * (3 - len(str(k)))}{k},{' ' * (3 - len(str(p[0])))}{p[0]})  "
                body += f" {p[1].main}  {p[1].name}\n"
        return header + body


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
