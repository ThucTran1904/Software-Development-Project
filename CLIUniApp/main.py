"""CLIUniApp entry point - the University System.

Run with:   python main.py      (from inside CLIUniApp/)
      or:   py -3 main.py

The University menu only routes between subsystems; all other work
is done by the controllers.
"""

from controllers import admin_controller, student_controller
from utils.term import say, ask, CYAN, YELLOW


UNI_PROMPT = "University System: (A)dmin, (S)tudent, or X : "


def main():
    while True:
        choice = ask(UNI_PROMPT, CYAN).strip().upper()
        if choice == "A":
            admin_controller.run()
        elif choice == "S":
            student_controller.run()
        elif choice == "X":
            say("Thank You", YELLOW)
            return


if __name__ == "__main__":
    main()
