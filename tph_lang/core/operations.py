general_symbols_tuple = (
    (">", "[move-right]"),
    ("<", "[move-left]"),
    ("^", "[move-up]"),
    ("v", "[move-down]"),
    ("V", "[move-down]"),
    ("@", "[end-program]"),
    ("$", "[erase-main-array]"),
    ("¢", "[erase-side-array]"),
    ("+", "[simple-sum]"),
    ("⨁", "[array-sum]"),
    ("D", "[array-sum]"),
    ("*", "[simple-multiplication]"),
    ("×", "[simple-multiplication]"),
    ("⨂", "[array-multiplication]"),
    ("X", "[array-multiplication]"),
    ("∘", "[outer-dot-multiplication]"),
    ("°", "[outer-dot-multiplication]"),
    ("∙", "[inner-dot-multiplication]"),
    ("•", "[inner-dot-multiplication]"),
    ("·", "[inner-dot-multiplication]"),
    ("c", "[copy]"),
    ("i", "[iota-range]"),
    ("ï", "[2iota-range]"),
    ("Ï", "[3iota-range]"),
    ("%", "[mod]"),
    ("|", "[logic-or]"),
    ("&", "[logic-and]"),
    ("¬", "[logic-not]"),
    ("~", "[logic-not]"),
    ("(", "[open-num]"),
    (")", "[close-num]"),
    ("b", "[input]"),
    ("r", "[output]"),
    (None, "[null]")
)

general_symbols_dict = {
    '>': '[move-right]',
    '<': '[move-left]',
    '^': '[move-up]',
    'v': '[move-down]',
    'V': '[move-down]',
    '@': '[end-program]',
    '$': '[erase-main-array]',
    '¢': '[erase-side-array]',
    '+': '[simple-sum]',
    '⨁': '[array-sum]',
    'D': '[array-sum]',
    '*': '[simple-multiplication]',
    '×': '[simple-multiplication]',
    '⨂': '[array-multiplication]',
    'X': '[array-multiplication]',
    '∘': '[outer-dot-multiplication]',
    '°': '[outer-dot-multiplication]',
    '∙': '[inner-dot-multiplication]',
    '•': '[inner-dot-multiplication]',
    '·': '[inner-dot-multiplication]',
    'c': '[copy]',
    'i': '[iota-range]',
    'ï': '[2iota-range]',
    'Ï': '[3iota-range]',
    '%': '[mod]',
    '|': '[logic-or]',
    '&': '[logic-and]',
    '¬': '[logic-not]',
    '~': '[logic-not]',
    '(': '[open-num]',
    ')': '[close-num]',
    'h': '[head]',
    't': '[tail]',
    'b': '[input]',
    'r': '[output]',
    None: '[null]'
}

name_std_dict = {
    "[move-right]": ">",
    "[move-left]": "<",
    "[move-up]": "^",
    "[move-down]": "v",
    "[end-program]": "@",
    "[erase-main-array]": "$",
    "[erase-side-array]": "¢",
    "[simple-sum]": "+",
    "[array-sum]": "D",
    "[simple-multiplication]": "*",
    "[array-multiplication]": "X",
    "[outer-dot-multiplication]": "°",
    "[inner-dot-multiplication]": "·",
    "[copy]": "c",
    "[iota-range]": "i",
    "[2iota-range]": "ï",
    "[3iota-range]": "Ï",
    "[simple-mod]": "%",
    "[logic-or]": "|",
    "[logic-and]": "&",
    "[logic-not]": "~",
    "[mod]": "%",
    "[open-num]": "(",
    "[close-num]": ")",
    "[head]": "h",
    "[tail]": "t",
    "[input]": "b",
    "[output]": "r",
    "[null]": None
}

literals_tuple = (
    (r"[0-9]", "[literal-integer]"),
)

directions = ["right", "left", "up", "down"]
scopes = ["main", "lhs", "rhs"]
