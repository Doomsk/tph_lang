from tph_lang.core.ast import AST


class Code:
    def __init__(self, code: AST):
        if isinstance(code, AST):
            self.code = code
            self.cur_pos = self.code.pos
        else:
            raise ValueError("code must be of type AST.")

