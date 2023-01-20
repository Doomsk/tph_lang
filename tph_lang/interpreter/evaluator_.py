from time import process_time
from tph_lang.interpreter.structures import Symbol, ArrayGroup


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

    def _handle_input(self, array, data, scope):
        words = data.replace('(', '').replace(')', '').replace(',', ' ').split(' ')
        for w in words:
            value = self.check_literal(w)
            # self.main_array.append(value)
            array[scope].append(value)
        return array

    def _find_next(self, cur_dir, cur_pos, pos):
        if cur_dir == "left":
            if self.code[cur_pos[0]].get_line(pos, False):
                return (cur_pos[0], pos), False
            if pos - 1 > 0:
                return self._find_next(cur_dir, cur_pos, pos - 1)
            return cur_pos, True
        if cur_dir == "right":
            if self.code[cur_pos[0]].get_line(pos, False):
                return (cur_pos[0], pos), False
            if any([pos < k for k in self.code.cols(cur_pos[0])]):
                return self._find_next(cur_dir, cur_pos, pos + 1)
            return cur_pos, True
        if cur_dir == "up":
            if self.code.get_line(pos, False):
                if self.code[pos].get_line(cur_pos[1], False):
                    return (pos, cur_pos[1]), False
                if any([pos - 1 <= k for k in self.lines]):
                    return self._find_next(cur_dir, cur_pos, pos - 1)
            return cur_pos, True
        if cur_dir == "down":
            if self.code.get_line(pos, False):
                if self.code[pos].get_line(cur_pos[1], False):
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

    def move(self, array, cur_pos, cur_dir, scope, extra=None):
        cur_dir, cur_pos, endline = self._move_next(cur_dir, cur_pos)
        if not endline:
            cur_value = self.code[cur_pos[0]][cur_pos[1]]
            return self.walk(array, cur_value, cur_dir, cur_pos, scope, extra)
        return array, extra, endline

    def go_next(self, array, cur_pos, cur_dir, scope, extra=None):
        return self.move(array, cur_pos, cur_dir, scope, extra)

    def peek_next(self, cur_dir, cur_pos):
        if cur_dir == "left":
            first_pos = cur_pos[1] - 1
            second_pos = cur_pos[0] - 1
            new_dir = "up"
        elif cur_dir == "right":
            first_pos = cur_pos[1] + 1
            second_pos = cur_pos[0] + 1
            new_dir = "down"
        elif cur_dir == "up":
            first_pos = cur_pos[0] - 1
            second_pos = cur_pos[1] + 1
            new_dir = "right"
        elif cur_dir == "down":
            first_pos = cur_pos[0] + 1
            second_pos = cur_pos[1] - 1
            new_dir = "left"
        else:
            raise ValueError(f"peek could not find cur_dir {cur_dir}.")

        new_pos, endline = self._find_next(cur_dir, cur_pos, first_pos)
        if not endline:
            return cur_dir, new_pos
        else:
            new_pos, endline = self._find_next(new_dir, cur_pos, second_pos)
            if not endline:
                return new_dir, new_pos
        raise ValueError("peek could not find where to go.")

    def look_side(self, array, cur_pos, cur_dir, scope, extra=None):
        if cur_dir == "right":
            cur_dir = "up"
        elif cur_dir == "left":
            cur_dir = "down"
        elif cur_dir == "up":
            cur_dir = "left"
        elif cur_dir == "down":
            cur_dir = "right"
        return self.go_next(array, cur_pos, cur_dir, scope, extra)

    def look_lhs(self, array, cur_dir, cur_pos, extra=None):
        return self.look_side(array, cur_dir, cur_pos, "lhs", extra)

    def look_rhs(self, array, cur_dir, cur_pos, extra=None):
        return self.look_side(array, cur_dir, cur_pos, "rhs", extra)

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

    def ast_literal(self, array, data, cur_pos, cur_dir, scope, extra=None):
        value = self.check_literal(data)
        # if scope == "main":
        #     self.main_array.append(value)
        # elif scope == "lhs":
        #     self.lhs_array.append(value)
        # elif scope == "rhs":
        #     self.rhs_array.append(value)
        array[scope].append(value)
        self.go_next(array, cur_pos, cur_dir, scope, extra)

    def ast_right(self, array, data, cur_pos, cur_dir, scope, extra=None):
        cur_dir = "right"
        self.go_next(array, cur_pos, cur_dir, scope, extra)

    def ast_left(self, array, data, cur_pos, cur_dir, scope, extra=None):
        cur_dir = "left"
        self.go_next(array, cur_pos, cur_dir, scope, extra)

    def ast_up(self, array, data, cur_pos, cur_dir, scope, extra=None):
        cur_dir = "up"
        self.go_next(array, cur_pos, cur_dir, scope, extra)

    def ast_down(self, array, data, cur_pos, cur_dir, scope, extra=None):
        cur_dir = "down"
        self.go_next(array, cur_pos, cur_dir, scope, extra)

    def ast_end(self, **args):
        self.t1 = process_time()
        print('-' * 30)
        print(f'@end program in {round(self.t1 - self.t0, 6)}s')

    def ast_simple_sum(self, array, data, cur_pos, cur_dir, scope, extra=None):
        # array = self.main_array if scope == "main" else self.lhs_array if scope == "lhs" else self.rhs_array
        # if all([isinstance(k, (int, float)) for k in array]):
        #     if scope == "main":
        #         self.main_array = [sum(array)]
        #     elif scope == "lhs":
        #         self.lhs_array = [sum(array)]
        #     elif scope == "rhs":
        #         self.rhs_array = [sum(array)]
        #     self.go_next(array, cur_pos, cur_dir, scope, extra)
        # else:
        #     print("simple-sum failed?")
        if all([isinstance(k, (int, float)) for k in array[scope]]):
            array[scope] = [sum(array[scope])]
        else:
            print("simple-sum failed!")

    def ast_array_sum(self, array, data, cur_pos, cur_dir, scope, extra=None):
        # # TODO: implement it properly
        # array = self.main_array if scope == "main" else self.lhs_array if scope == "lhs" else self.rhs_array
        # if all([isinstance(k, (int, float)) for k in array]):
        #     if scope == "main":
        #         self.look_lhs(cur_dir, cur_pos, extra)
        #         if len(self.lhs_array) == 1:
        #             data = self.lhs_array[0]
        #             self.main_array = [m + data for m in self.main_array]
        #         else:
        #             self.main_array = [m + n for m, n in zip(self.main_array, self.lhs_array)]
        #
        #         if self.side_erase:
        #             self.lhs_array = []
        #             self.side_erase = False
        #         self.go_next(array, cur_pos, cur_dir, scope, extra)
        #     else:
        #         raise NotImplementedError("cannot array-sum outside 'main' scope yet.")
        if all([isinstance(k, (int, float)) for k in array["main"]]):
            self.look_lhs(array, cur_dir, cur_pos, extra)
            if len(array["lhs"]) == 1:
                value = array["lhs"][0]
                array["main"] = [m + value for m in array["main"]]
            else:
                array["main"] = [m + n for m, n in zip(array["main"], array["lhs"])]

            if self.side_erase:
                array["lhs"] = []
                self.side_erase = False
            self.go_next(array, cur_pos, cur_dir, scope, extra)
        else:
            raise NotImplementedError("cannot array-sum other than int/float values.")

    def ast_dot(self, array, data, cur_pos, cur_dir, scope, extra=None):
        pass

    def ast_copy(self, array, data, cur_pos, cur_dir, scope, extra=None):
        # if scope == "main":
        #     self.main_array.extend(self.main_array)
        # elif scope == "lhs":
        #     self.lhs_array.extend(self.main_array)
        # elif scope == "rhs":
        #     self.rhs_array.extend(self.main_array)
        new_array = ArrayGroup("main")
        new_array, extra = self.look_lhs(new_array, cur_dir, cur_pos, extra)
        # if len(new_array["main"]) > 0:
        array[scope].extend(array["main"])
        self.go_next(array, cur_pos, cur_dir, scope, extra)

    def ast_mod(self, array, data, cur_pos, cur_dir, scope, extra=None):
        if cur_dir == "right":
            self.go_next(array, "up", cur_pos, "lhs", data)
        elif cur_dir == "left":
            self.go_next(array, "down", cur_pos, "lhs", data)
        elif cur_dir == "up":
            self.go_next(array, "left", cur_pos, "lhs", data)
        elif cur_dir == "down":
            self.go_next(array, "right", cur_pos, "lhs", data)
        if self.perform_oper:
            self.dyadic_mod()
            if self.side_erase:
                # self.lhs_array = []
                array["lhs"] = []
                self.side_erase = False
        else:
            self.perform_oper = True
        new_dir, _ = self.peek_next(cur_dir, cur_pos)
        if cur_dir != new_dir:
            self.main_array, self.rhs_array = self.rhs_array, []
        self.go_next(array, new_dir, cur_pos, scope, extra)

    # def dyadic_mod(self, array, **kwargs):
    #     # TODO: generalize for all scopes (currently for main)
    #     new_main = []
    #     if oper := kwargs.get("oper", False):
    #         for k in self.main_array:
    #             if not self.dyadics.get(oper, self.ast_null)(*(k % p == 0 for p in self.lhs_array)):
    #                 self.rhs_array.append(k)
    #             else:
    #                 new_main.append(k)
    #     else:
    #         for k in self.main_array:
    #             if not k % self.lhs_array[0] == 0:
    #                 self.rhs_array.append(k)
    #             else:
    #                 new_main.append(k)
    #     self.main_array = new_main

    def dyadic_mod(self, array, scope, oper=None):
        new_main = []
        if oper is not None:
            for k in array[scope]:
                pass


    def ast_iota(self, array, data, cur_pos, cur_dir, scope, extra=None):
        if scope == "main":
            if data == Symbol("i"):
                value = self.main_array.pop(0)
                array = [m for m in range(value)]
                self.main_array.extend(array)
            self.go_next(array, cur_pos, cur_dir, scope, extra)
        else:
            raise NotImplementedError("need to implement iota for scopes other than 'main'.")

    def ast_and(self, array, data, cur_pos, cur_dir, scope, extra=None):
        if scope == "main":
            pass
        elif scope == "lhs":
            self.dyadics.get(extra, self.ast_null)(oper=data)
            self.perform_oper = False
            self.lhs_array = []
        elif scope == "rhs":
            pass
        self.go_next(array, cur_pos, cur_dir, scope, extra)

    @staticmethod
    def dyadic_and(*args):
        return all(args)

    def ast_or(self, array, data, cur_pos, cur_dir, scope, extra=None):
        if scope == "main":
            pass
        elif scope == "lhs":
            # initial approach
            self.dyadics.get(extra, self.ast_null)(oper=data)
            self.perform_oper = False
            self.lhs_array = []
        elif scope == "rhs":
            pass
        return self.go_next(array, cur_pos, cur_dir, scope, extra)

    @staticmethod
    def dyadic_or(*args):
        return any(args)

    def ast_not(self, array, data, cur_pos, cur_dir, scope, extra=None):
        # if scope == "main":
        #     self.main_array = [not k for k in self.main_array]
        # elif scope == "lhs":
        #     self.lhs_array = [not k for k in self.lhs_array]
        # elif scope == "rhs":
        #     self.rhs_array = [not k for k in self.rhs_array]
        array[scope] = [not k for k in array[scope]]
        return self.go_next(array, cur_pos, cur_dir, scope, extra)

    def ast_input(self, array, data, cur_pos, cur_dir, scope, extra=None):
        answer = input(": ")
        array = self._handle_input(array, answer, scope)
        new_array, new_extra = self.go_next(array, cur_pos, cur_dir, scope, extra)
        return new_array, new_extra

    def ast_output(self, array, data, cur_pos, cur_dir, scope, extra=None):
        # if scope == "main":
        #     res = self.main_array
        # elif scope == "lhs":
        #     res = self.lhs_array
        # elif scope == "rhs":
        #     res = self.rhs_array
        # else:
        #     res = []
        # print(*res)
        print(*array[scope])
        new_array, new_extra = self.go_next(array, cur_pos, cur_dir, scope, extra)
        return new_array, new_extra

    def ast_erase(self, array, data, cur_pos, cur_dir, scope, extra=None):
        # if scope == "main":
        #     self.main_array = []
        # elif scope == "lhs":
        #     self.lhs_array = []
        # elif scope == "rhs":
        #     self.rhs_array = []
        array["main"] = []
        new_array, new_extra = self.go_next(array, cur_pos, cur_dir, scope, extra)
        return new_array, new_extra

    def ast_side_erase(self, array, data, cur_pos, cur_dir, scope, extra=None):
        # self.side_erase = True
        array["lhs"] = []
        return self.go_next(array, cur_pos, cur_dir, scope, extra)

    def ast_check(self, array, data, cur_pos, cur_dir, scope, extra=None):
        return (self.ast_literal if data.isnumeric() else self.ast_null)(
            array,
            data,
            cur_dir,
            cur_pos,
            scope,
            extra
        )

    @staticmethod
    def ast_null(*args):
        return ArrayGroup(args[4]), None

    def walk(self, array, cur_value, cur_dir, cur_pos, scope, extra=None):
        return self.nodes.get(cur_value, self.ast_check)(
            array,
            cur_value,
            cur_dir,
            cur_pos,
            scope,
            extra
        )

    def run(self):
        print()
        self.t0 = process_time()
        cur_value = self.code[self.cur_pos[0]][self.cur_pos[1]]
        scope = "main"
        array = ArrayGroup("main")
        self.walk(array, cur_value, self.cur_dir, self.cur_pos, scope)