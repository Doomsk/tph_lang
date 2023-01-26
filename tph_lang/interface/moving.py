from copy import deepcopy
import PySimpleGUI as pg
from tph_lang.interface.code import Code
from tph_lang.interface import (
    CODE_FONT,
    INIT_POS,
    INIT_DIR,
    MODES,
    INIT_MODE,
    W_OFFSET,
    H_OFFSET,
    MODE_COLORS,
    MODE_KEYS,
    PASS_KEYS,
    CODE_SPACE_SIZE
)


class MovingCell:
    cur_dir = INIT_DIR
    cur_pos = INIT_POS
    prev_pos = INIT_POS
    reverse_dir = {"right": "left", "left": "right", "up": "down", "down": "up"}
    move_keys = ["Right", "Left", "Down", "Up"]
    move_keys_dict = {"R": ">", "L": "<", "U": "^", "D": "v"}
    move_keys_dir = {">": "right", "<": "left", "^": "up", "v": "down"}

    def move_next_cell(self):
        if self.cur_dir == "right":
            self.cur_pos = self.cur_pos[0] + W_OFFSET, self.cur_pos[1]
        elif self.cur_dir == "left":
            self.cur_pos = self.cur_pos[0] - W_OFFSET, self.cur_pos[1]
        elif self.cur_dir == "up":
            self.cur_pos = self.cur_pos[0], self.cur_pos[1] - H_OFFSET
        elif self.cur_dir == "down":
            self.cur_pos = self.cur_pos[0], self.cur_pos[1] + H_OFFSET


class MovingLineCol:
    cur_mode = INIT_MODE

    def __init__(self, board: pg.Graph, pos):
        self.board = board
        self.cur_pos = pos
        self.line_key = self.create_line()
        self.col_key = self.create_col()

    def move_line(self, prev_pos, cur_pos):
        self.board.move_figure(
            self.line_key,
            x_direction=0,
            y_direction=cur_pos[1] - prev_pos[1]
        )
        self.board.send_figure_to_back(self.line_key)

    def move_col(self, prev_pos, cur_pos):
        self.board.move_figure(
            self.col_key,
            x_direction=cur_pos[0] - prev_pos[0],
            y_direction=0
        )
        self.board.send_figure_to_back(self.col_key)

    def move(self, prev_pos, cur_pos):
        self.move_line(prev_pos, cur_pos)
        self.move_col(prev_pos, cur_pos)

    def create_line(self):
        return self.board.draw_rectangle(
            top_left=(1, 2 + self.cur_pos[1] - INIT_POS[1]),
            bottom_right=(CODE_SPACE_SIZE[0], 5 + H_OFFSET + self.cur_pos[1] - INIT_POS[1]),
            fill_color=MODE_COLORS[self.cur_mode]["linecol"]
        )

    def create_col(self):
        return self.board.draw_rectangle(
            top_left=(1 + self.cur_pos[0] - INIT_POS[0], 1),
            bottom_right=(3 + W_OFFSET + self.cur_pos[0] - INIT_POS[0], CODE_SPACE_SIZE[1]),
            fill_color=MODE_COLORS[self.cur_mode]["linecol"]
        )

    def create_linecol(self, pos=None):
        if pos is not None:
            self.cur_pos = deepcopy(pos)
        self.line_key = self.create_line()
        self.col_key = self.create_col()

    def update_linecol_mode(self, pos):
        self.board.delete_figure(self.line_key)
        self.board.delete_figure(self.col_key)
        self.cur_pos = deepcopy(pos)
        self.create_linecol()
        self.board.send_figure_to_back(self.line_key)
        self.board.send_figure_to_back(self.col_key)

    def toggle_linecol_mode(self, cur_pos=None):
        self.cur_mode = MODES[1] if self.cur_mode == MODES[0] else MODES[0]
        if cur_pos is not None:
            self.cur_pos = deepcopy(cur_pos)
        self.update_linecol_mode(self.cur_pos)


class MovingCursor(MovingCell):
    cur_mode = INIT_MODE
    top_shift = -6
    bottom_shift = 6
    left_shift = -11
    right_shift = 11

    def __init__(self, board: pg.Graph):
        self.board = board
        self.linecol = MovingLineCol(self.board, self.cur_pos)
        self.cursor_key = self.create_cursor()

    def create_cursor(self) -> int:
        return self.board.draw_rectangle(
            top_left=(self.cur_pos[0] + self.top_shift, self.cur_pos[1] + self.left_shift),
            bottom_right=(self.cur_pos[0] + self.bottom_shift, self.cur_pos[1] + self.right_shift),
            fill_color=MODE_COLORS[self.cur_mode]["cursor"]
        )

    def update_cursor_mode(self):
        self.board.delete_figure(self.cursor_key)
        self.cur_pos = deepcopy(self.prev_pos)
        self.cursor_key = self.create_cursor()
        self.board.send_figure_to_back(self.cursor_key)

    def move_cursor(self):
        self.board.move_figure(
            self.cursor_key,
            x_direction=self.cur_pos[0] - self.prev_pos[0],
            y_direction=self.cur_pos[1] - self.prev_pos[1]
        )
        self.board.send_figure_to_back(self.cursor_key)
        self.linecol.move(self.prev_pos, self.cur_pos)

    def toggle_mode(self):
        self.cur_mode = MODES[1] if self.cur_mode == MODES[0] else MODES[0]
        self.update_cursor_mode()
        self.linecol.toggle_linecol_mode(self.cur_pos)


class MovingChar(MovingCursor):
    def __init__(self, board: pg.Graph):
        super().__init__(board)
        self.code = Code()

    def draw_char(self, event: str):
        return self.board.draw_text(event, location=self.cur_pos, font=CODE_FONT)

    def add_dir(self, item: str):
        new_item = item.lower()
        self.cur_dir = self.move_keys_dir[new_item]
        if self.cur_pos in self.code.code_pos:
            val, idx = self.code.pop(self.cur_pos)
            last_char = self.code[-1]
            self.board.delete_figure(val[1])
            if new_item != last_char[0] and self.cur_dir != last_char[-1]:
                key = self.draw_char(new_item)
                self.code.insert(idx, (new_item, key, self.prev_pos, self.cur_dir))
        else:
            last_char = self.code[-1]
            if new_item != last_char[0] and self.cur_dir != last_char[-1]:
                key = self.draw_char(new_item)
                self.code += (new_item, key, self.prev_pos, self.cur_dir)
        self.move_next_cell()
        self.move_cursor()
        self.prev_pos = deepcopy(self.cur_pos)

    def move_dir(self, item: str):
        new_item = item.lower()
        self.cur_dir = self.move_keys_dir[new_item]
        self.move_next_cell()
        self.move_cursor()
        self.prev_pos = deepcopy(self.cur_pos)

    def add_char(self, item: str):
        if self.cur_pos in self.code.code_pos:
            val, idx = self.code.pop(self.cur_pos)
            self.cur_dir = val[-1]
            self.board.delete_figure(val[1])
            key = self.draw_char(item)
            self.move_cursor()
            self.prev_pos = deepcopy(self.cur_pos)
            self.move_next_cell()
            self.code.insert(idx, (item, key, self.prev_pos, self.cur_dir))
        else:
            key = self.draw_char(item)
            self.move_cursor()
            self.prev_pos = deepcopy(self.cur_pos)
            self.move_next_cell()
            self.code += (item, key, self.prev_pos, self.cur_dir)

    def take_event(self, event: str):
        item = event.split(':')[0]
        if self.cur_mode == MODES[0]:
            # in case the key is a backspace
            if item == "BackSpace":
                pass
            # to move the position
            elif item in self.move_keys:
                self.add_dir(self.move_keys_dict[item[0]])
            # to toggle modes (code, view)
            elif item in MODE_KEYS:
                self.toggle_mode()
            # to actually print the key pressed
            elif item not in PASS_KEYS:
                self.add_char(item)
            else:
                pass
        # self.cur_mode == "view"
        else:
            if item in MODE_KEYS:
                self.toggle_mode()
            elif item in self.move_keys:
                self.move_dir(self.move_keys_dict[item[0]])

        # print(self.code)
