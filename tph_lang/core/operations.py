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
    ("o", "[outer-dot-multiplication"),
    ("∙", "[inner-dot-multiplication]"),
    ("•", "[inner-dot-multiplication]"),
    ("·", "[inner-dot-multiplication]"),
    (".", "[inner-dot-multiplication]"),
    ("c", "[copy]"),
    ("i", "[iota-range]"),
    ("ï", "[2iota-range]"),
    ("Ï", "[3iota-range]"),
    ("%", "[simple-mod]"),
    ("|", "[logic-or]"),
    ("&", "[logic-and]"),
    ("¬", "[logic-not]"),
    ("~", "[logic-not]"),
    ("b", "[input]"),
    ("r", "[output]"),
)

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
    "[simple-multiplication]": "x",
    "[array-multiplication]": "X",
    "[outer-dot-multiplication]": "o",
    "[inner-dot-multiplication]": ".",
    "[copy]": "c",
    "[iota-range]": "i",
    "[2iota-range]": "ï",
    "[3iota-range]": "Ï",
    "[simple-mod]": "%",
    "[logic-or]": "|",
    "[logic-and]": "&",
    "[logic-not]": "~",
    "[input]": "b",
    "[output]": "r"
}

literals_tuple = (
    (r"[0-9]", "[literal-integer]"),
)