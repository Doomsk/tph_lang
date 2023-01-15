import os
from .ast import AST
from .cst import CST

file_dir = os.path.dirname(__file__)

grammar = open(os.path.join(file_dir, "grammar.peg"), "r").read()
