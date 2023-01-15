from arpeggio.cleanpeg import ParserPEG
from arpeggio import visit_parse_tree
from tph_lang.core.cst import CST
from tph_lang.core import grammar


def get_linecol(code):
    line = 1
    col = 1
    tokens = []
    for k in code:
        if k == " ":
            col += 1
        elif k == "\n":
            line += 1
            col = 1
        else:
            tokens.append((k, line, col))
            col += 1
    return tokens


def parsing(code):
    tk = get_linecol(code)
    parser = ParserPEG(grammar, "program", debug=False, reduce_tree=True, skipws=True)
    pt = parser.parse(code)
    return visit_parse_tree(pt, CST(tokens=tk))
