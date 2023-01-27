from copy import deepcopy
from typing import Any
from tph_lang.core import (
    DirS,
    OperS,
    LiteralS
)
from tph_lang.core.ast2 import AST, Symbol
from tph_lang.interpreter.moving import Mover
from tph_lang.interpreter.structures import ArrayGroup
import tph_lang.interpreter.literals2 as lit
import tph_lang.interpreter.operators as oper


class Eval:
    def __init__(self, code: AST):
        self.code = self.check_code(code)
        self.tokens = {
            OperS.END_PROGRAM: oper.EndProgram(),
            OperS.INPUT: oper.Input(),
            OperS.OUTPUT: oper.Output(),
            OperS.SIMPLE_SUM: oper.SimpleSum(),
            LiteralS.DIGIT: lit.Int(),
        }

    @staticmethod
    def check_code(data):
        if isinstance(data, AST):
            return data
        raise ValueError(f"code must be parsed and of type tph_lang.core.ast.AST.")

    def walk(self, code: [AST, str], array: ArrayGroup, scope):
        if isinstance(code, str):
            return array
        if code.has_lhs():
            array = self.walk(code.lhs, array, scope)
        if code.has_rhs():
            if code.has_main():
                print("yay main + rhs")
            else:
                print("yay rhs, no main")
                # new_array = ArrayGroup(scope="main", cur_pos=code.pos, cur_dir=code.dir)
                # new_array.main = array.rhs
                # self.tokens[code.name](self.walk(code.rhs, array, scope))
        else:
            if code.has_main():
                print(f"has main {code} -> {code.main}")
                array = self.tokens[code.name](array)
                array = self.walk(code.main, array, scope)
            else:
                print("unknown")
        return array

    def run(self):
        cur_pos = self.code.pos
        cur_dir = self.code.dir
        scope = "main"
        array = ArrayGroup(scope=scope, cur_pos=cur_pos, cur_dir=cur_dir)
        self.walk(self.code, array, scope)
