import os
from enum import Enum, auto

# from .ast import AST
# from .cst import CST

file_dir = os.path.dirname(__file__)

grammar = open(os.path.join(file_dir, "grammar.peg"), "r").read()


class AllSymbols(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


class ScopeS(AllSymbols):
    MAIN = auto()
    LHS = auto()
    RHS = auto()


class LiteralS(AllSymbols):
    DIGIT = auto()
    INT = auto()
    STR = auto()
    FLOAT = auto()
    COMPLEX = auto()


class DirS(AllSymbols):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


class OperS(AllSymbols):
    END_PROGRAM = auto()
    SIMPLE_SUM = auto()
    DIRECT_SUM = auto()
    SIMPLE_MULT = auto()
    ARRAY_MULT = auto()
    OUTER_MULT = auto()
    INNER_MULT = auto()
    COPY = auto()
    IOTA_RANGE = auto()
    MOD = auto()
    OR = auto()
    AND = auto()
    NOT = auto()
    OPEN = auto()
    CLOSE = auto()
    QUOTE = auto()
    HEAD = auto()
    TAIL = auto()
    INPUT = auto()
    OUTPUT = auto()
    DOT_MARK = auto()


# directions list
DIR_LIST = [DirS.RIGHT, DirS.LEFT, DirS.UP, DirS.DOWN]

# left hand side orientation
LHS_REL = {
    DirS.RIGHT: DirS.UP,
    DirS.LEFT: DirS.DOWN,
    DirS.UP: DirS.LEFT,
    DirS.DOWN: DirS.RIGHT
}

# right hand side orientation
RHS_REL = {
    DirS.RIGHT: DirS.DOWN,
    DirS.LEFT: DirS.UP,
    DirS.UP: DirS.RIGHT,
    DirS.DOWN: DirS.LEFT
}

# Main In Main Out: operators with 1 input and 1 output
MIMO = (
    OperS.END_PROGRAM,
    OperS.SIMPLE_SUM,
    OperS.SIMPLE_MULT,
    OperS.OPEN,
    OperS.CLOSE,
    OperS.HEAD,
    OperS.TAIL,
    OperS.AND,
    OperS.OR,
    OperS.NOT,
    OperS.INPUT,
    OperS.OUTPUT
)

# Main In Main & RHS Out: operators with 1 input and 2 outputs
MIMRO = (

)

# Main & LHS In Main Out: operators with 2 inputs and 1 output
MLIMO = (
    OperS.DIRECT_SUM,
    OperS.ARRAY_MULT,
    OperS.COPY,
    OperS.IOTA_RANGE,
    OperS.MOD,
)

# Main & LHS In RHS Out: operators with 2 inputs and 1 output
MLIRO = (
    OperS.IOTA_RANGE,
    OperS.MOD
)

# Main & LHS & RHS In Main Out: operators with 3 inputs and 1 output
MLRIMO = (

)

opers_dict = {
    ">": DirS.RIGHT,
    "<": DirS.LEFT,
    "^": DirS.UP,
    "v": DirS.DOWN,
    "V": DirS.DOWN,
    "@": OperS.END_PROGRAM,
    "%": OperS.MOD,
    "(": OperS.OPEN,
    ")": OperS.CLOSE,
    "c": OperS.COPY,
    "i": OperS.IOTA_RANGE,
    "b": OperS.INPUT,
    "r": OperS.OUTPUT,
    "~": OperS.NOT,
    "&": OperS.AND,
    "|": OperS.OR,
    "h": OperS.HEAD,
    "t": OperS.TAIL,
    "\"": OperS.QUOTE,
    "+": OperS.SIMPLE_SUM,
    "D": OperS.DIRECT_SUM,
    "*": OperS.SIMPLE_MULT,
    "X": OperS.ARRAY_MULT,
    "°": OperS.OUTER_MULT,
    "·": OperS.INNER_MULT,
    ".": OperS.DOT_MARK
}

int_literal = (r"[0-9]", LiteralS.DIGIT)

str_literal = (r".+", LiteralS.STR)
