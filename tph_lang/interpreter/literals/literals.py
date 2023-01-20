from abc import ABC, abstractmethod
from tph_lang.core.ast import AST


class Literals(ABC):
    pass


class IntegerLiteral(Literals):
    pass


class FloatLiteral(Literals):
    pass


class ComplexLiteral(Literals):
    pass


class StringLiteral(Literals):
    pass
