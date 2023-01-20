from tph_lang.core.ast import AST
from tph_lang.core.operations import (directions, scopes)


class Mover:
    to_lhs = {"right": "up", "left": "down", "up": "left", "down": "right"}
    to_rhs = {"right": "down", "left": "up", "up": "right", "down": "left"}

    def __init__(self, code: AST):
        self.lines = dict()
        self.cols = dict()
        self.extract_moves(code)

    def extract_moves(self, data: AST):
        self.lines = {k: list(map(lambda x: x[0], v)) for k, v in data}
        for k, v in data:
            for p, q in v:
                if p not in self.cols.keys():
                    self.cols.update({p: [k]})
                else:
                    self.cols[p].append(k)

    def _find_next(self, cur_pos: tuple, cur_dir: str) -> (tuple, bool):
        """
        given a position and a direction,
        returns the next position with endline as False.

        if no next position is available in the direction,
        returns the same position with endline as True.

        :param cur_pos: tuple of two integers as (line, col)
        :param cur_dir: one of the four directions
        :return: cur_pos, endline
        """
        if cur_dir == "right":
            index_col = (col := self.lines[cur_pos[0]]).index(cur_pos[1])
            if index_col + 1 < len(col):
                return (cur_pos[0], col[index_col+1]), False
            return cur_pos, True
        elif cur_dir == "left":
            index_col = (col := self.lines[cur_pos[0]]).index(cur_pos[1])
            if index_col - 1 >= 0:
                return (cur_pos[0], col[index_col - 1]), False
            return cur_pos, True
        elif cur_dir == "up":
            index_col = (line := self.cols[cur_pos[1]]).index(cur_pos[0])
            if index_col - 1 >= 0:
                return (line[index_col - 1], cur_pos[1]), False
            return cur_pos, True
        elif cur_dir == "down":
            index_col = (line := self.cols[cur_pos[1]]).index(cur_pos[0])
            if index_col + 1 < len(line):
                return (line[index_col + 1], cur_pos[1]), False
            return cur_pos, True

    def go_next(self, cur_pos: tuple, cur_dir: str) -> (tuple, bool):
        if cur_pos[0] in self.lines.keys() and cur_pos[1] in self.cols.keys():
            if cur_dir in directions:
                return self._find_next(cur_pos, cur_dir)
            raise ValueError(f"wrong direction given '{cur_dir}'.")
        raise ValueError(f"invalid position given '{cur_pos}'.")

    def peek_next(self, cur_pos: tuple, cur_dir: str) -> (tuple, bool):
        new_pos, endline = self.go_next(cur_pos, cur_dir)
        if not endline:
            return new_pos, cur_dir
        new_dir = self.to_rhs[cur_dir]
        new_pos, _ = self.go_next(cur_pos, new_dir)
        return new_pos, new_dir

    def look_lhs(self, cur_pos, cur_dir):
        return self.go_next(cur_pos, self.to_lhs[cur_dir])

    def look_rhs(self, cur_pos, cur_dir):
        return self.go_next(cur_pos, self.to_rhs[cur_dir])

    def look_around(self, cur_pos, cur_dir):
        lhs = self.look_lhs(cur_pos, cur_dir)
        rhs = self.look_rhs(cur_pos, cur_dir)
        return {"lhs": lhs[0] if not lhs[1] else (), "rhs": rhs[0] if not rhs[1] else ()}
