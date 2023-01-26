import PySimpleGUI as pg
from tph_lang.interface.moving import MovingChar
from tph_lang.interface.layouts import (gen_main_layout, update_linecol)
from tph_lang.interface import (INIT_POS, INIT_MODE)


def run_gui():
    window = pg.Window(
        "tph editor",
        gen_main_layout(INIT_POS, INIT_MODE),
        return_keyboard_events=True,
        finalize=True
    )
    board = window["board"]
    gui_on = True
    cur_char = MovingChar(board)

    while gui_on:
        event, values = window.read()
        old_mode = cur_char.cur_mode
        print(event)
        if event in [pg.WIN_CLOSED, pg.WINDOW_CLOSED]:
            gui_on = not gui_on
        else:
            cur_char.take_event(event)

        if cur_char.cur_mode != old_mode:
            window[f"radio_{cur_char.cur_mode}"].update(value=True)
            window["frame_mode"].update(value=f"[{cur_char.cur_mode}]")
        window["linecol"].update(value=update_linecol(cur_char.prev_pos))
    window.close()


if __name__ == "__main__":
    run_gui()
