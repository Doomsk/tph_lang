# default fonts
TITLE_FONT =  "Menlo 13"
CODE_FONT = "Menlo 12"
LINECOL_FONT = "Menlo 11"

# initial position on editor for moving and coloring
INIT_POS = (8, 12)

# initial direction for the cursor
INIT_DIR = "right"

# possible modes (edit, view)
MODES = ["edit", "view"]

# initial mode (edit or view)
INIT_MODE = "edit"

# offsets defined according to editor font size
W_OFFSET = 12
H_OFFSET = 18

# colors
CODE_LINECOL_COLOR = "#f4bec3"
VIEW_LINECOL_COLOR = "#bedeff"
CUR_CODE_COLOR = "#ed8385"
CUR_VIEW_COLOR = "#c7c6ff"

# modes and colors
MODE_COLORS = {
    "edit": {
        "cursor": CUR_CODE_COLOR,
        "linecol": CODE_LINECOL_COLOR
    },
    "view": {
        "cursor": CUR_VIEW_COLOR,
        "linecol": VIEW_LINECOL_COLOR
    }
}

# key for control mode
MODE_KEYS = ["Control_L", "Control_R", "radio_edit", "radio_view"]

# keys to ignore on code editor input
PASS_KEYS = [
    "board",
    "Shift_L",
    "Shift_R",
    "Return",
    "Control_L",
    "Control_R",
    "Tab",
    "Caps_Lock",
    "Meta",
    "Alt_L",
    "Alt_R",
    " ",
    "Escape",
    "Super",
    "nobreakspace",
    "BackSpace",
    ">",
    "V",
    "v",
    "<",
    "??"
]

# interface code space size
CODE_SPACE_SIZE = (490, 420)
CODE_SPACE_COORD = [(0, 420), (490, 0)]
# first value is the number of characters, the second is in pixels
CODE_SPACE_H_SLIDER = (70, 5)
CODE_SPACE_V_SLIDER = (25, 15)

# sizer distance from left to right so line/col text can be justified on the right
SIZER_LINECOL = (350, 12)
