from time import process_time
from tph_lang.core.structures import Symbol


# noinspection PyArgumentList
class Eval:
    def __init__(self, code):
        self.code = code
        self.main_array = []
        self.lhs_array = []
        self.rhs_array = []
        self.cur_dir = "right"
        self.cur_pos = self.code.pos
        self.side_erase = False
        self.cur_value = ''
        self.perform_oper = True
        self.t0 = 0
        self.t1 = 0
        self.lines = self.code.lines()
        self.nodes = {
            Symbol(">"): self.ast_right,
            Symbol("<"): self.ast_left,
            Symbol("^"): self.ast_up,
            Symbol("v"): self.ast_down,
            Symbol("@"): self.ast_end,
            Symbol("+"): self.ast_simple_sum,
            Symbol("D"): self.ast_array_sum,
            Symbol("."): self.ast_dot,
            Symbol("c"): self.ast_copy,
            Symbol("%"): self.ast_mod,
            Symbol("i"): self.ast_iota,
            Symbol("|"): self.ast_or,
            Symbol("&"): self.ast_and,
            Symbol("~"): self.ast_not,
            Symbol("b"): self.ast_input,
            Symbol("r"): self.ast_output,
            Symbol("$"): self.ast_erase,
            Symbol("¢"): self.ast_side_erase
        }
        self.dyadics = {
            Symbol("%"): self.dyadic_mod,
            Symbol("|"): self.dyadic_or,
            Symbol("&"): self.dyadic_and,
            None: self.ast_null
        }

    def _handle_input(self, data):
        words = data.replace('(', '').replace(')', '').replace(',', ' ').split(' ')
        for w in words:
            value = self.check_literal(w)
            self.main_array.append(value)

    def _find_next(self, cur_dir, cur_pos, pos):
        if cur_dir == "left":
            if self.code[cur_pos[0]].get(pos, False):
                return (cur_pos[0], pos), False
            if pos - 1 > 0:
                return self._find_next(cur_dir, cur_pos, pos - 1)
            return cur_pos, True
        if cur_dir == "right":
            if self.code[cur_pos[0]].get(pos, False):
                return (cur_pos[0], pos), False
            if any([pos < k for k in self.code.cols(cur_pos[0])]):
                return self._find_next(cur_dir, cur_pos, pos + 1)
            return cur_pos, True
        if cur_dir == "up":
            if self.code.get(pos, False):
                if self.code[pos].get(cur_pos[1], False):
                    return (pos, cur_pos[1]), False
                if pos - 1 > 0:
                    return self._find_next(cur_dir, cur_pos, pos - 1)
                return self._find_next(cur_dir, cur_pos, self.lines[-1])
            return cur_pos, True
        if cur_dir == "down":
            if self.code.get(pos, False):
                if self.code[pos].get(cur_pos[1], False):
                    return (pos, cur_pos[1]), False
                if any([pos + 1 <= k for k in self.lines]):
                    return self._find_next(cur_dir, cur_pos, pos + 1)
                return cur_pos, True
            return self._find_next(cur_dir, cur_pos, pos + 1)
        raise ValueError("oh no! something went wrong")

    def _move_next(self, cur_dir, cur_pos):
        if cur_dir == "left":
            cur_pos, endline = self._find_next(cur_dir, cur_pos, cur_pos[1] - 1)
        elif cur_dir == "right":
            cur_pos, endline = self._find_next(cur_dir, cur_pos, cur_pos[1] + 1)
        elif cur_dir == "up":
            cur_pos, endline = self._find_next(cur_dir, cur_pos, cur_pos[0] - 1)
        elif cur_dir == "down":
            cur_pos, endline = self._find_next(cur_dir, cur_pos, cur_pos[0] + 1)
        else:
            print("wut?")
            endline = True
        return cur_dir, cur_pos, endline

    def main_move(self, *args, **kwargs):
        self.cur_dir, self.cur_pos, endline = self._move_next(self.cur_dir, self.cur_pos)
        if not endline:
            self.cur_value = self.code[self.cur_pos[0]][self.cur_pos[1]]
            self.walk(self.cur_value, self.cur_dir, self.cur_pos, "main", kwargs.get("extra", None))

    def sec_move(self, cur_dir, cur_pos, scope, extra=None):
        cur_dir, cur_pos, endline = self._move_next(cur_dir, cur_pos)
        if not endline:
            cur_value = self.code[cur_pos[0]][cur_pos[1]]
            self.walk(cur_value, cur_dir, cur_pos, scope, extra)

    def go_next(self, cur_dir, cur_pos, scope, extra=None):
        self.main_move(extra=extra) if scope == "main" else self.sec_move(cur_dir, cur_pos, scope,
                                                                          extra)

    def look_side(self, cur_dir, cur_pos, scope, extra=None):
        if cur_dir == "right":
            cur_dir = "up"
        elif cur_dir == "left":
            cur_dir = "down"
        elif cur_dir == "up":
            cur_dir = "left"
        elif cur_dir == "down":
            cur_dir = "right"
        self.go_next(cur_dir, cur_pos, scope, extra)

    def look_lhs(self, cur_dir, cur_pos, extra=None):
        self.look_side(cur_dir, cur_pos, "lhs", extra)

    def look_rhs(self, cur_dir, cur_pos, extra=None):
        self.look_side(cur_dir, cur_pos, "rhs", extra)

    @staticmethod
    def get_int(data):
        if isinstance(data, Symbol):
            try:
                return int(data.value)
            except ValueError:
                raise ValueError()
        if isinstance(data, str):
            try:
                return int(data)
            except ValueError:
                raise ValueError()

    def check_literal(self, data):
        try:
            value = self.get_int(data)
        except ValueError as e:
            raise ValueError(f"something went wrong on literal value... {e}.")
        else:
            return value

    def ast_literal(self, data, cur_dir, cur_pos, scope, extra=None):
        value = self.check_literal(data)
        if scope == "main":
            self.main_array.append(value)
        elif scope == "lhs":
            self.lhs_array.append(value)
        elif scope == "rhs":
            self.rhs_array.append(value)
        self.go_next(cur_dir, cur_pos, scope, extra)

    def ast_right(self, data, cur_dir, cur_pos, scope, extra=None):
        if scope == "main":
            self.cur_dir = "right"
            self.go_next(self.cur_dir, cur_pos, scope, extra)

    def ast_left(self, data, cur_dir, cur_pos, scope, extra=None):
        if scope == "main":
            self.cur_dir = "left"
            self.go_next(self.cur_dir, cur_pos, scope, extra)

    def ast_up(self, data, cur_dir, cur_pos, scope, extra=None):
        if scope == "main":
            self.cur_dir = "up"
            self.go_next(self.cur_dir, cur_pos, scope, extra)

    def ast_down(self, data, cur_dir, cur_pos, scope, extra=None):
        if scope == "main":
            self.cur_dir = "down"
            self.go_next(self.cur_dir, cur_pos, scope, extra)

    def ast_end(self, data, cur_dir, cur_pos, scope, extra=None):
        self.t1 = process_time()
        print('-' * 30)
        print(f'@end program in {round(self.t1 - self.t0, 6)}s')

    def ast_simple_sum(self, data, cur_dir, cur_pos, scope, extra=None):
        array = self.main_array if scope == "main" else self.lhs_array if scope == "lhs" else self.rhs_array
        if all([isinstance(k, (int, float)) for k in array]):
            if scope == "main":
                self.main_array = [sum(array)]
            elif scope == "lhs":
                self.lhs_array = [sum(array)]
            elif scope == "rhs":
                self.rhs_array = [sum(array)]
            self.go_next(cur_dir, cur_pos, scope, extra)
        else:
            print("simple-sum failed?")

    def ast_array_sum(self, data, cur_dir, cur_pos, scope, extra=None):
        # TODO: implement it properly
        array = self.main_array if scope == "main" else self.lhs_array if scope == "lhs" else self.rhs_array
        if all([isinstance(k, (int, float)) for k in array]):
            if scope == "main":
                self.look_lhs(cur_dir, cur_pos, extra)
                if len(self.lhs_array) == 1:
                    data = self.lhs_array[0]
                    self.main_array = [m + data for m in self.main_array]
                else:
                    self.main_array = [m + n for m, n in zip(self.main_array, self.lhs_array)]

                if self.side_erase:
                    self.lhs_array = []
                    self.side_erase = False
                self.go_next(cur_dir, cur_pos, scope, extra)
            else:
                raise NotImplementedError("cannot array-sum outside 'main' scope yet.")

    def ast_dot(self, data, cur_dir, cur_pos, scope, extra=None):
        pass

    def ast_copy(self, data, cur_dir, cur_pos, scope, extra=None):
        if scope == "main":
            self.main_array.extend(self.main_array)
        elif scope == "lhs":
            self.lhs_array.extend(self.main_array)
        elif scope == "rhs":
            self.rhs_array.extend(self.main_array)
        self.go_next(cur_dir, cur_pos, scope, extra)

    def ast_mod(self, data, cur_dir, cur_pos, scope, extra=None):
        if cur_dir == "right":
            self.go_next("up", cur_pos, "lhs", data)
        elif cur_dir == "left":
            self.go_next("down", cur_pos, "lhs", data)
        elif cur_dir == "up":
            self.go_next("left", cur_pos, "lhs", data)
        elif cur_dir == "down":
            self.go_next("right", cur_pos, "lhs", data)
        if self.perform_oper:
            self.dyadic_mod()
        else:
            self.perform_oper = True
        self.go_next(cur_dir, cur_pos, scope, extra)

    def dyadic_mod(self, **kwargs):
        # TODO: generalize for all scopes (currently for main)
        new_main = []
        if oper := kwargs.get("oper", False):
            for k in self.main_array:
                if not self.dyadics.get(oper, self.ast_null)(*(k % p == 0 for p in self.lhs_array)):
                    self.rhs_array.append(k)
                else:
                    new_main.append(k)
        else:
            for k in self.main_array:
                if not k % self.lhs_array[0] == 0:
                    self.rhs_array.append(k)
                else:
                    new_main.append(k)
        self.main_array = new_main

    def ast_iota(self, data, cur_dir, cur_pos, scope, extra=None):
        if scope == "main":
            if data == Symbol("i"):
                value = self.main_array.pop(0)
                array = [m for m in range(value)]
                self.main_array.extend(array)
            self.go_next(cur_dir, cur_pos, scope, extra)
        else:
            raise NotImplementedError("need to implement iota for scopes other than 'main'.")

    def ast_and(self, data, cur_dir, cur_pos, scope, extra=None):
        pass

    @staticmethod
    def dyadic_and(*args):
        return all(args)

    def ast_or(self, data, cur_dir, cur_pos, scope, extra=None):
        if scope == "main":
            pass
        elif scope == "lhs":
            self.dyadics.get(extra, self.ast_null)(oper=data)
            self.perform_oper = False
        elif scope == "rhs":
            pass
        self.go_next(cur_dir, cur_pos, scope, extra)

    @staticmethod
    def dyadic_or(*args):
        return any(args)

    def ast_not(self, data, cur_dir, cur_pos, scope, extra=None):
        pass

    def ast_input(self, data, cur_dir, cur_pos, scope, extra=None):
        answer = input(": ")
        self._handle_input(answer)
        self.go_next(cur_dir, cur_pos, scope, extra)

    def ast_output(self, data, cur_dir, cur_pos, scope, extra=None):
        print(*self.main_array)
        self.go_next(cur_dir, cur_pos, scope, extra)

    def ast_erase(self, data, cur_dir, cur_pos, scope, extra=None):
        if scope == "main":
            self.main_array = []
        elif scope == "lhs":
            self.lhs_array = []
        elif scope == "rhs":
            self.rhs_array = []
        self.go_next(cur_dir, cur_pos, scope, extra)

    def ast_side_erase(self, data, cur_dir, cur_pos, scope, extra=None):
        self.side_erase = True

    def ast_check(self, data, cur_dir, cur_pos, scope, extra=None):
        (self.ast_literal if data.isnumeric() else self.ast_null)(data, cur_dir, cur_pos, scope,
                                                                  extra)

    @staticmethod
    def ast_null(*args):
        pass

    def walk(self, cur_value, cur_dir, cur_pos, scope, extra=None):
        self.nodes.get(cur_value, self.ast_check)(cur_value, cur_dir, cur_pos, scope, extra)

    def run(self):
        print()
        self.t0 = process_time()
        cur_value = self.code[self.cur_pos[0]][self.cur_pos[1]]
        scope = "main"
        self.walk(cur_value, self.cur_dir, self.cur_pos, scope)
