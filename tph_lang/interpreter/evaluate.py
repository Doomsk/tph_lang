import sys
import click
from tph_lang.core.parser import parsing
from .evaluator import Eval
from tph_lang import __version__


def run(code, print_parse=False):
    _p = parsing(code)
    if print_parse:
        print(_p)
    Eval(_p).run()


@click.group(invoke_without_command=True, context_settings=dict(ignore_unknown_options=True))
@click.argument("file", type=click.Path(exists=True), required=False)
@click.option("-v", "version", is_flag=True)
def run2(file, version):
    if version:
        click.echo(f"H-hat version {__version__}")
    else:
        code = open(file, "r").read()
        run(code)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_ = sys.argv[1]
        with open(file_, "r") as f:
            code_ = f
            run(code_)
