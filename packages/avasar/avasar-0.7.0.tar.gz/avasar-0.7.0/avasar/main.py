from .dsl import build_context
import code
from rlcompleter import Completer
import readline
from pathlib import Path
from os.path import expanduser
import sys


def run():
    context = build_context()
    context.__dict__["set_groups"] = context._set_groups
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            print(context.fstr("{gen.character}"))
            sys.exit(0)

    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    readline.set_completer(Completer(context.__dict__).complete)

    history = Path(expanduser("~/.avasar_history"))
    try:
        readline.read_history_file(history)
    except OSError:
        pass
    try:
        code.InteractiveConsole(context.__dict__).interact()
    finally:
        readline.set_history_length(1000)
        readline.write_history_file(history)
