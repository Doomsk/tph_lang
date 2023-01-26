from copy import deepcopy
from tph_lang.core.ast import AST
from tph_lang.interpreter.moving import Mover
from tph_lang.interpreter.literals import check_literal
from tph_lang.interpreter.structures import (ArrayGroup, Symbol)


class Eval:
    def __init__(self, code: AST):
        self.code = self.check_code(code)
        self.cell = Mover(code)
        self.moves = {
            "[move-right]": self.ast_right,
            "[move-left]": self.ast_left,
            "[move-up]": self.ast_up,
            "[move-down]": self.ast_down,
        }
        self.nodes = {
            "[end-program]": self.ast_endprogram,
            "[mod]": self.ast_mod,
            "[iota-range]": self.ast_iota,
            "[copy]": self.ast_copy,
            "[open-num]": self.ast_open_num,
            "[close-num]": self.ast_close_num,
            "[head]": self.ast_head,
            "[tail]": self.ast_tail,
            "[input]": self.ast_input,
            "[output]": self.ast_output
        }

    @staticmethod
    def check_code(data):
        if isinstance(data, AST):
            return data
        raise ValueError(f"code must be parsed and of type tph_lang.core.ast.AST.")

    def ast_check(self, code, array, scope):
        pass

    def walk(self, code, array, scope):
        n = code.name
        self.moves.get(n, self.nodes.get(n, self.ast_check))(code, array, scope)

    def run(self):
        pass
