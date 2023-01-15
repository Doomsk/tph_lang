from arpeggio import PTNodeVisitor
from tph_lang.core.ast import AST


class CST(PTNodeVisitor):
    def __init__(self, tokens, defaults=True, **kwargs):
        super().__init__(defaults=defaults, **kwargs)
        self.tokens = tokens

    def generic(self, n, k):
        val = self.tokens.pop(0)
        return AST(n.value, n.value, val[1:])

    def visit_program(self, n, k):
        return AST("program", k)

    def visit_dir(self, n, k):
        return self.generic(n, k)

    def visit_oper(self, n, k):
        return self.generic(n, k)

    def visit_sum(self, n, k):
        return self.generic(n, k)

    def visit_mult(self, n, k):
        return self.generic(n, k)

    def visit_io(self, n, k):
        return self.generic(n, k)

    def visit_copy(self, n, k):
        return self.generic(n,k)

    def visit_range(self, n, k):
        return self.generic(n, k)

    def visit_mod(self, n, k):
        return self.generic(n, k)

    def visit_logic_oper(self, n, k):
        return self.generic(n, k)

    def visit_erase(self, n, k):
        return self.generic(n, k)

    def visit_end(self, n, k):
        return self.generic(n, k)

    def visit_int(self, n, k):
        return self.generic(n, k)