from tph_lang.core.ast2 import AST, Symbol
from tph_lang.core import (
    DirS,
    OperS,
    LHS_REL,
    RHS_REL,
    LiteralS,
    MIMO,
    MIMRO,
    MLIMO,
    MLIRO,
    MLRIMO
)


class SimpleParser:
    def __init__(self, code: str):
        self.code = code
        self.cur_dir = DirS.RIGHT
        self.pos_data, self.line_data, self.col_data, self.start_pos = self.get_linecols()

    def get_linecols(self):
        line = 1
        col = 1
        pos_dict = dict()
        lines_dict = dict()
        cols_dict = dict()
        first_pos = ()
        is_first = True
        open_quote = False
        for k in self.code:
            if k == " ":
                col += 1
            elif k == "\n":
                line += 1
                col = 1
            else:
                if is_first:
                    first_pos = (line, col)
                    is_first = False
                if k == "\"":
                    open_quote = True if not open_quote else False
                symbol = Symbol(k, prev_char=OperS.QUOTE if open_quote else None)
                pos_dict.update({(line, col): symbol})
                if line in lines_dict.keys():
                    lines_dict[line].append(col)
                else:
                    lines_dict.update({line: [col]})

                if col in cols_dict.keys():
                    cols_dict[col].append(line)
                else:
                    cols_dict.update({col: [line]})
                col += 1
        return pos_dict, lines_dict, cols_dict, first_pos

    def parse(self, line=None, col=None, cur_dir=None) -> AST:
        parsed_lhs = None
        parsed_rhs = None
        if line is None and col is None:
            line, col = self.start_pos
        if cur_dir is None:
            cur_dir = self.cur_dir
        cell = self.pos_data[(line, col)]
        if cell.name in [DirS.RIGHT, DirS.LEFT, DirS.UP, DirS.DOWN]:
            cur_dir = cell.name
            line, col = self.next_cell((line, col), cur_dir)
            parsed = self.parse(line, col, cur_dir)
            return AST(cell.name, (line, col), cur_dir, parsed)
        else:
            if self.check_lhs((line, col), cur_dir, cell.name):
                new_line, new_col = self.next_cell((line, col), LHS_REL[cur_dir])
                parsed_lhs = self.parse(new_line, new_col, LHS_REL[cur_dir])

            if self.check_rhs((line, col), cur_dir, cell.name):
                new_line, new_col = self.next_cell((line, col), RHS_REL[cur_dir])
                if not self.check_main((line, col), cur_dir):
                    parsed = self.parse(new_line, new_col, RHS_REL[cur_dir])
                else:
                    parsed_rhs = self.parse(new_line, new_col, RHS_REL[cur_dir])
                    parsed = self.parse(new_line, new_col, cur_dir)
            else:
                if self.check_main((line, col), cur_dir):
                    new_line, new_col = self.next_cell((line, col), cur_dir)
                    parsed = self.parse(new_line, new_col, cur_dir)
                else:
                    return AST(cell.name, (line, col), cur_dir, cell.value)
            return AST(cell.name, (line, col), cur_dir, parsed, parsed_lhs, parsed_rhs)

    def next_cell(self, pos, cur_dir):
        if cur_dir == DirS.RIGHT:
            line = self.line_data[pos[0]]
            idx_col = line.index(pos[1])
            if idx_col + 1 < len(line):
                return pos[0], line[idx_col + 1]
            return ()
        if cur_dir == DirS.LEFT:
            line = self.line_data[pos[0]]
            idx_col = line.index(pos[1])
            if idx_col - 1 >= 0:
                return pos[0], line[idx_col - 1]
            return ()
        if cur_dir == DirS.DOWN:
            col = self.col_data[pos[1]]
            idx_line = col.index(pos[0])
            if idx_line + 1 < len(col):
                return col[idx_line + 1], pos[1]
            return ()
        if cur_dir == DirS.UP:
            col = self.col_data[pos[1]]
            idx_line = col.index(pos[0])
            if idx_line - 1 >= 0:
                return col[idx_line - 1], pos[1]
            return ()
        else:
            raise ValueError(f"wrong direction '{cur_dir}'.")

    def check_main(self, pos, cur_dir):
        return True if self.next_cell(pos, cur_dir) else False

    def check_lhs(self, pos, cur_dir, name):
        if name in MLIMO or name in MLIRO or name in MLRIMO:
            return True if self.next_cell(pos, LHS_REL[cur_dir]) else False
        else:
            return False

    def check_rhs(self, pos, cur_dir, name):
        if name in MIMRO or name in MLIRO or name in MLRIMO:
            return True if self.next_cell(pos, RHS_REL[cur_dir]) else False
        else:
            return False
