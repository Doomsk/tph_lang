from tph_lang.interpreter.structures import Symbol


class AST:
    def __init__(self, name, value, pos=None):
        self.name = name
        self.value = self.build_values(value, pos)
        self.pos = pos if pos else (self.lines()[0], self.cols(self.lines()[0])[0])

    def build_values(self, data, pos):
        if self.name != "program":
            return {pos[0]: {pos[1]: Symbol(data)}}
        values = dict()
        for p in data:
            for k, v in p.value.items():
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
                body += f" {p[1].value}  {p[1].name}\n"
        return header + body
