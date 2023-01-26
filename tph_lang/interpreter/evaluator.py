from copy import deepcopy
from tph_lang.core.ast import AST
from tph_lang.interpreter.moving import Mover
from tph_lang.interpreter.literals import check_literal
from tph_lang.interpreter.structures import (ArrayGroup, Symbol)


# noinspection PyArgumentList
class Eval:
    def __init__(self, code: AST):
        self.code = self.check_code(code)
        self.walker = Mover(code)
        self.nodes = {
            "[move-right]": self.ast_right,
            "[move-left]": self.ast_left,
            "[move-up]": self.ast_up,
            "[move-down]": self.ast_down,
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
        self.metacode = {
            "[mod]": self.meta_mod,
            "[iota-range]": self.meta_iota,
            "[open-num]": self.meta_open_num,
            "[close-num]": self.meta_close_num,
            "[copy]": self.meta_copy,
            "[head]": self.meta_head,
            "[tail]": self.meta_tail,
            "[input]": self.meta_input,
            "[output]": self.meta_output
        }
        self.monads = {}
        self.dyads = {}
        self.literals = check_literal

    @staticmethod
    def check_code(data):
        if isinstance(data, AST):
            return data
        raise ValueError(f"code must be parsed and of type tph_lang.core.ast.AST.")

    ###################
    # EXTRA FUNCTIONS #
    ###################

    @staticmethod
    def def_extra(data=None):
        if isinstance(data, (str, Symbol)):
            return [dict(oper=data, value=0)]
        return []

    @staticmethod
    def check_extra(extra, data):
        value = "oper" if isinstance(data, str) else "value"
        if len(extra) > 0:
            return extra[-1].get(value, Symbol(None))
        return Symbol(None)

    @staticmethod
    def append_extra(extra, data):
        extra.append({"oper": data, "value": 0})

    @staticmethod
    def pop_extra(extra, pos=0):
        if len(extra) > 0:
            return extra.pop(pos if pos < len(extra) else 0)
        return dict(oper=Symbol(None).name, value=0)

    @staticmethod
    def assign_extra(extra, key, data):
        if key in extra[-1].keys():
            extra[-1][key] = data

    @staticmethod
    def inc_value_extra(extra):
        extra[-1]["value"] += 1

    #####################
    # EXECUTE FUNCTIONS #
    #####################

    def execute_direction(self, array, scope, extra):
        new_pos, endline = self.walker.go_next(array.cur_pos, array.cur_dir)
        if not endline:
            array.cur_pos = new_pos
            code = self.code.get(new_pos)
            self.walk(code, array, scope, extra)
        else:
            raise ValueError(f"no code found on {array.cur_dir} direction.")

    def execute_next(self, code, array, scope, extra):
        new_pos, endline = self.walker.go_next(array.cur_pos, array.cur_dir)
        print(f"next: new pos {code} {new_pos} {array.cur_dir} {extra} {endline} {scope}")
        if not endline:
            array.cur_pos = new_pos
            code = self.code.get(new_pos)
            self.walk(code, array, scope, extra)

    def execute_metamonad(self, code, array, scope, extra):
        print(code.name, code.value, array.cur_pos, array.cur_dir, scope)
        self.metacode.get(code.name, self.meta_null)(code, array, scope, extra)

    def execute_metadyad(self, code, array, scope, extra):
        print(code.name, code.value, array.cur_pos, array.cur_dir, extra, scope)
        data = self.walker.look_around(array.cur_pos, array.cur_dir)
        self.append_extra(extra, code)
        if data["lhs"]:
            print(f"{code.name}: lhs found")
            if scope in ["lhs", "rhs"]:
                print('new array lhs')
                new_array = ArrayGroup(
                    scope="main",
                    cur_pos=array.cur_pos,
                    cur_dir=array.cur_dir,
                    marginal=True
                )
                new_array.main = array.from_scope[scope].copy()
                self.walk_lhs(new_array, "main", extra)
            else:
                self.walk_lhs(array, "lhs", extra)
                self.pop_extra(extra)
        print(f"before meta {array.main} {array.lhs} {array.rhs} {array.cur_dir}")
        self.metacode.get(code.name)(code, array, scope, extra)
        print(f"after meta {array.main} {array.lhs} {array.rhs} {array.cur_dir}")
        array.lhs.clean()

    def execute_metatriad(self, code, array, scope, extra):
        print(code.name, code.value, array.cur_pos, array.cur_dir, scope)
        data = self.walker.look_around(array.cur_pos, array.cur_dir)
        new_extra = self.def_extra(code)
        if data["rhs"]:
            print(f"{code.name}: rhs found")
            self.walk_rhs(array, scope, new_extra)
        if data["lhs"]:
            print(f"{code.name}: lhs found")
            self.walk_lhs(array, scope, new_extra)
        if len(extra) > 0:
            print(self.metacode)

    def execute_auxiliary_path(self, new_scope, array, scope, extra):
        if new_scope == "lhs":
            new_dir = self.walker.to_lhs[array.cur_dir]
        else:  # new_scope == "rhs"
            new_dir = self.walker.to_rhs[array.cur_dir]
        new_pos, endline = self.walker.go_next(cur_pos=array.cur_pos, cur_dir=new_dir)
        print(f"aux path {array.cur_pos} {new_pos} {new_dir} {endline}")
        new_code = self.code.get(new_pos)
        array.cur_pos = new_pos
        array.cur_dir = new_dir
        self.walk(new_code, array, new_scope, extra)

    ##################
    # META FUNCTIONS #
    ##################

    # TODO: move this section to respective classes in monad, dyad, etc files

    def meta_null(self, *args, **kwargs):
        return False

    def meta_input(self, code, array, scope, extra):
        data = input(": ")
        words = data.replace('(', '').replace(')', '').replace(',', ' ').split(' ')
        for w in words:
            if val := check_literal(w):
                array.from_scope[scope].append(val)

    def meta_output(self, code, array, scope, extra):
        print(*array.from_scope[scope])

    def meta_open_num(self, code, array, scope, extra):
        pass

    def meta_close_num(self, code, array, scope, extra):
        pass

    def meta_mod(self, code, array, scope, extra):
        if len(array.main) > 0 and len(array.lhs) > 0:
            tmp_main = []
            if len(extra) > 0:
                oper = self.pop_extra(extra)["oper"]
                for p in array.main:
                    if self.metacode.get(oper, self.meta_null)(*[p % k == 0 for k in array.lhs]):
                        tmp_main.append(p)
                    else:
                        array.rhs.append(p)
            else:
                for p in array.main:
                    if p % array.lhs[-1] == 0:
                        tmp_main.append(p)
                    else:
                        array.rhs.append(p)
            array.main = tmp_main

    def meta_iota(self, code, array, scope, extra):
        if len(array.from_scope[scope]) > 0:
            value = array.from_scope[scope].pop(0)
            array.from_scope[scope].extend([n for n in range(value)])
        else:
            raise ValueError("cannot perform 'iota' on empty array.")

    def meta_copy(self, core, array, scope, extra):
        if len(array.main) > 0:
            if len(extra) > 0:
                oper = self.pop_extra(extra)["oper"]
            else:
                array.lhs.extend(deepcopy(array.main))

    def meta_head(self, core, array, scope, extra):
        if scope == "main" and len(array.main) > 0:
            value = array.main.pop(-1)
        elif len(array.from_scope[scope]) > 0:
            value = array.from_scope[scope].pop(-1)
        else:
            raise ValueError("no head!")
        if len(extra) > 0:
            return array.main[:value]
        array.main = array.main[:value]

    def meta_tail(self, core, array, scope, extra):
        print('tail?')
        if len(array.main) > 0:
            value = array.from_scope[scope].pop(-1)
            print(f'tail {value} {array.main[-value:]}')
        else:
            raise ValueError("no tail!")
        # if len(extra) > 0:
        #     return deepcopy(array.main[-value:])
        if scope == "main":
            array.main = array.main[-value:]
        else:
            array.from_scope[scope].extend(deepcopy(array.main[-value:]))

    #################
    # AST FUNCTIONS #
    #################

    def ast_right(self, code, array, scope, extra):
        print(code.name, code.value, array.cur_pos, array.cur_dir)
        array.cur_dir = "right"
        self.execute_direction(array, scope, extra)

    def ast_left(self, code, array, scope, extra):
        print(code.name, code.value, array.cur_pos, array.cur_dir)
        array.cur_dir = "left"
        self.execute_direction(array, scope, extra)

    def ast_up(self, code, array, scope, extra):
        print(code.name, code.value, array.cur_pos, array.cur_dir)
        array.cur_dir = "up"
        self.execute_direction(array, scope, extra)

    def ast_down(self, code, array, scope, extra):
        print(code.name, code.value, array.cur_pos, array.cur_dir)
        array.cur_dir = "down"
        self.execute_direction(array, scope, extra)

    def ast_mod(self, code, array, scope, extra):
        old_pos, old_dir = array.flush()
        self.execute_metadyad(code, array, scope, extra)
        array.cur_pos, array.cur_dir = old_pos, old_dir
        _, new_dir = self.walker.peek_next(array.cur_pos, array.cur_dir)
        if new_dir != array.cur_dir:
            array.cur_dir = new_dir
            array.main.swap(array.rhs)
            array.rhs.clean()
        self.execute_next(code, array, scope, extra)

    def ast_iota(self, code, array, scope, extra):
        old_pos, old_dir = array.flush()
        self.execute_metamonad(code, array, scope, extra)
        array.cur_pos, array.cur_dir = old_pos, old_dir
        self.execute_next(code, array, scope, extra)

    def ast_copy(self, code, array, scope, extra):
        old_pos, old_dir = array.flush()
        self.execute_metadyad(code, array, scope, extra)
        array.cur_pos, array.cur_dir = old_pos, old_dir
        self.execute_next(code, array, scope, extra)

    def ast_open_num(self, code, array, scope, extra):
        extra = self.def_extra(code)
        self.execute_metamonad(code, array, scope, extra)
        self.execute_next(code, array, scope, extra)

    def ast_close_num(self, code, array, scope, extra):
        self.execute_metamonad(code, array, scope, extra)
        self.execute_next(code, array, scope, extra)

    def ast_head(self, code, array, scope, extra):
        old_pos, old_dir = array.flush()
        self.execute_metamonad(code, array, scope, extra)
        array.cur_pos, array.cur_dir = old_pos, old_dir
        self.execute_next(code, array, scope, extra)

    def ast_tail(self, code, array, scope, extra):
        print('tail?')
        old_pos, old_dir = array.flush()
        self.execute_metamonad(code, array, scope, extra)
        array.cur_pos, array.cur_dir = old_pos, old_dir
        self.execute_next(code, array, scope, extra)

    def ast_input(self, code, array, scope, extra):
        old_pos, old_dir = array.flush()
        self.execute_metamonad(code, array, scope, extra)
        array.cur_pos, array.cur_dir = old_pos, old_dir
        self.execute_next(code, array, scope, extra)

    def ast_output(self, code, array, scope, extra):
        old_pos, old_dir = array.flush()
        self.execute_metamonad(code, array, scope, extra)
        array.cur_pos, array.cur_dir = old_pos, old_dir
        self.execute_next(code, array, scope, extra)

    def ast_endprogram(self, code, array, scope, extra):
        print("@end program.")
        print(array.main)
        print(array.lhs)
        print(array.rhs)

    def null(self, *args, **kwargs):
        pass

    def ast_check(self, code, array, scope, extra):
        c = self.check_extra(extra, 'oper')
        print(f"ast check {code} {c} {type(c)} {c.__hash__()}")
        if (check := self.check_extra(extra, "oper")) == Symbol("("):
            if self.check_extra(extra, "value"):
                # extra["value"] += 1
                self.inc_value_extra(extra)
            else:
                # extra.update({"value": 1})
                self.assign_extra(extra, "value", 1)
            array.main.append(code.value)
        elif check.name in self.nodes.keys():
            if lit := check_literal(code):
                print(f"ha! [{code}]", lit, array.cur_pos, array.cur_dir, scope)
                array.from_scope[scope].append(lit)
        else:
            if lit := check_literal(code):
                print(lit, array.cur_pos, array.cur_dir, scope)
                array.main.append(lit)
            else:
                print('nothing literal here?')
        self.execute_next(code, array, scope, extra)

    ##################
    # WALK FUNCTIONS #
    ##################

    def walk_lhs(self, array: ArrayGroup, scope: str, extra):
        self.execute_auxiliary_path("lhs", array, scope, extra)

    def walk_rhs(self, array: ArrayGroup, scope: str, extra):
        if scope in ["lhs", "rhs"]:
            print('new array rhs')
            array = ArrayGroup(scope="main", cur_pos=array.cur_pos, cur_dir=array.cur_dir, marginal=True)
        self.execute_auxiliary_path("rhs", array, scope, extra)

    def walk(self, code: AST, array: ArrayGroup, scope: str, extra):
        print(f'walk {code} =>{extra}')
        if oper := self.check_extra(extra, "oper"):
            print('extra oper?')
            (self.nodes.get(code.name, self.ast_check))(code, array, scope, extra)
        else:
            print('extra no oper')
            (self.nodes.get(code.name, self.ast_check))(code, array, scope, extra)

    #######
    # RUN #
    #######

    def run(self):
        cur_pos = self.code.pos
        cur_dir = "right"
        scope = "main"
        array = ArrayGroup(scope="main", cur_pos=cur_pos, cur_dir=cur_dir)
        code = self.code.get(cur_pos)
        extra = self.def_extra(None)
        self.walk(code, array, scope, extra)
