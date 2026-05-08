"""GUIUniApp entry point.

Launches the login window. The login window is the main Tk window;
other windows (enrolment, subjects, exception) are Toplevels opened
from it.

The GUI shares the same students.data file as CLIUniApp via the
Database class inside CLIUniApp. We add that folder to sys.path so
a student registered from the CLI can log into the GUI straight away.
"""

import os
import sys
import tkinter as tk

HERE = os.path.dirname(os.path.abspath(__file__))
CLI_DIR = os.path.abspath(os.path.join(HERE, "..", "CLIUniApp"))
if CLI_DIR not in sys.path:
    sys.path.insert(0, CLI_DIR)

from windows.login_window import LoginWindow


def main():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
