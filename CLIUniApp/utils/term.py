"""Tiny terminal helper - ANSI colours plus colour-aware print/input.

The Sample I/O in the assessment PDF uses four colours:

    cyan   - the top-level University System prompt
    green  - sub-system prompts and section headings
    yellow - info / success messages
    red    - errors and the destructive "clear database" confirmation

We use raw ANSI escape codes so we don't need a third-party library
(colorama or similar). On Windows 10+ the classic console understands
VT sequences once any program writes them, and the no-op ``os.system("")``
call below reliably enables that mode if it isn't already on.

Disable colours by setting the environment variable NO_COLOR before
launching the program.
"""

import os
import sys


CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def _colours_enabled():
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        # don't dump escape codes into a redirected log/file
        return False
    return True


_USE_COLOUR = _colours_enabled()

if _USE_COLOUR and sys.platform == "win32":
    # turn on virtual-terminal processing on legacy Windows consoles
    os.system("")


def _wrap(text, colour):
    if not _USE_COLOUR or colour is None:
        return text
    return f"{colour}{text}{RESET}"


def say(text, colour=None):
    """Print ``text`` in ``colour`` and finish with a reset."""
    print(_wrap(text, colour))


def ask(prompt, colour=None):
    """Print ``prompt`` in ``colour``, read a line, then reset.

    Sending RESET after ``input()`` returns ensures any subsequent print
    starts in the default colour, regardless of which colour the prompt
    used.
    """
    if not _USE_COLOUR or colour is None:
        return input(prompt)
    try:
        return input(f"{colour}{prompt}")
    finally:
        sys.stdout.write(RESET)
        sys.stdout.flush()
