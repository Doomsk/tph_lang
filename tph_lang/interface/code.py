

class Code:
    code_chars = []
    code_keys = dict()
    code_pos = dict()

    # TODO: implement the plain text code generator
    def gen_final_code(self) -> str:
        pass

    # TODO: implement the save text code to file (.tph)
    def save_code2file(self):
        pass

    def pop(self, index):
        if isinstance(index, int):
            if index < len(self.code_chars):
                val = self.code_chars.pop(index)
                self.code_keys.pop(val[1])
                self.code_pos.pop(val[2])
                return val, index
        if isinstance(index, tuple):
            val = self.code_pos.pop(index)
            self.code_keys.pop(val[1])
            idx = self.code_chars.index(val)
            self.code_chars.pop(idx)
            return val, idx
        raise ValueError(f"code interface does not have index '{index}'.")

    def insert(self, index, item):
        self.code_chars.insert(index, item)
        self.code_keys.update({item[1]: item})
        self.code_pos.update({item[2]: item})

    def key(self, item):
        return self.code_keys.get(item, None)

    def pos(self, item):
        return self.code_pos.get(item, None)

    def __add__(self, other):
        if isinstance(other, tuple):
            self.code_chars.append(other)
            self.code_keys.update({other[1]: other})
            self.code_pos.update({other[2]: other})
            return self
        raise ValueError(f"code interface cannot add '{other}'.")

    def __iadd__(self, other):
        return self.__add__(other)

    def __iter__(self):
        yield from self.code_chars

    def __len__(self):
        return len(self.code_chars)

    def __contains__(self, item):
        if isinstance(item, int):
            return item in self.code_keys.keys()
        if isinstance(item, tuple):
            return item in self.code_pos.keys()
        raise ValueError(f"code interface cannot check '{item}'.")

    def __getitem__(self, item):
        return self.code_chars[item]

    def __repr__(self):
        chars_list = ", ".join([f'(char: {k[0]} | key: {k[1]} | pos: {k[2]} | dir: {k[3]})' for k in self.code_chars])
        return f"({chars_list})"
