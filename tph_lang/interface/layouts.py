import PySimpleGUI as pg
from tph_lang.interface import (
    TITLE_FONT,
    CODE_FONT,
    LINECOL_FONT,
    MODES,
    INIT_MODE,
    INIT_POS,
    W_OFFSET,
    H_OFFSET,
    CODE_SPACE_SIZE,
    CODE_SPACE_COORD,
    CODE_SPACE_H_SLIDER,
    CODE_SPACE_V_SLIDER,
    SIZER_LINECOL
)


def gen_modes_layout(mode):
    return [
        pg.Text("mode: ", font=CODE_FONT),
        pg.Radio(
            MODES[0],
            "radio_mode",
            default=True,
            enable_events=True,
            key="radio_edit",
            font=CODE_FONT
        ),
        pg.Radio(
            MODES[1],
            "radio_mode",
            enable_events=True,
            key="radio_view",
            font=CODE_FONT
        ),
        pg.Text(
            "- press CTRL to toggle between modes",
            font=CODE_FONT
        )
    ]


def linecol_str_space(value):
    str_value = str(value)
    return ' ' * (3 - len(str_value)) + str_value


def update_linecol(pos):
    line_num = int((pos[1] - INIT_POS[1]) / H_OFFSET + 1)
    col_num = int((pos[0] - INIT_POS[0]) / W_OFFSET + 1)
    return f"line: {linecol_str_space(line_num)} | col: {linecol_str_space(col_num)}"


def gen_code_space(pos):
    linecol_text = update_linecol(pos)
    return [
        [pg.Graph(
            CODE_SPACE_SIZE,
            graph_bottom_left=CODE_SPACE_COORD[0],
            graph_top_right=CODE_SPACE_COORD[1],
            background_color="white",
            enable_events=True,
            key="board"
        ),
            pg.Slider(
                range=(0, 0),
                size=CODE_SPACE_V_SLIDER,
                disabled=True,
                resolution=5,
                orientation="v",
                enable_events=True,
                visible=True,
                disable_number_display=True,
                key="v_slider"
            )],
        [pg.Slider(
            range=(0, 0),
            size=CODE_SPACE_H_SLIDER,
            disabled=True,
            resolution=5,
            orientation="h",
            enable_events=True,
            visible=True,
            disable_number_display=True,
            key="h_slider"
        )],
        [pg.Sizer(SIZER_LINECOL[0], SIZER_LINECOL[1]),
         pg.Text(
             linecol_text,
             auto_size_text=True,
             text_color="white",
             font=CODE_FONT,
             key="linecol"
         )]
    ]


# noinspection PyTypeChecker
def gen_editor_layout(pos, mode=INIT_MODE):
    return [
        pg.Frame(
            f"[{mode}]",
            gen_code_space(pos),
            title_location=pg.TITLE_LOCATION_TOP,
            font=TITLE_FONT,
            key="frame_mode"
        )
    ]


def gen_board_layout(pos, mode):
    return [gen_modes_layout(mode), gen_editor_layout(pos, mode)]


def gen_main_layout(pos, mode):
    return [[
        pg.Frame(
            "magic board",
            gen_board_layout(pos, mode),
            font=TITLE_FONT
        )
    ]]
