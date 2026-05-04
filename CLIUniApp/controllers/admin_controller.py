"""Admin System menu - show / group / partition / remove / clear.

Admins don't log in, so the menu is available immediately after the
user chooses 'A' at the University prompt. Every line is indented 8
spaces to sit one level under the University menu; empty-state
messages sit one level deeper (16 spaces) to match the Sample I/O.
"""

from database import Database
from utils.term import say, ask, GREEN, YELLOW, RED


INDENT = " " * 8
DEEPER = " " * 16
MENU_PROMPT = INDENT + "Admin System (c/g/p/r/s/x): "
GRADE_ORDER = ["Z", "P", "C", "D", "HD"]


def run():
    db = Database()
    while True:
        choice = ask(MENU_PROMPT, GREEN).strip().lower()
        if choice == "s":
            _show_all(db)
        elif choice == "g":
            _group_by_grade(db)
        elif choice == "p":
            _partition(db)
        elif choice == "r":
            _remove(db)
        elif choice == "c":
            _clear(db)
        elif choice == "x":
            return


def _show_all(db):
    students = db.read_all()
    say(INDENT + "Student List", GREEN)
    if not students:
        say(DEEPER + "< Nothing to Display >")
        return
    for s in students:
        say(INDENT + f"{s.name} :: {s.id} --> Email: {s.email}")


def _group_by_grade(db):
    students = db.read_all()
    say(INDENT + "Grade Grouping", GREEN)
    if not students:
        say(DEEPER + "< Nothing to Display >")
        return

    groups = {}
    for s in students:
        groups.setdefault(s.overall_grade(), []).append(s)

    for grade in GRADE_ORDER:
        if grade not in groups:
            continue
        rows = ", ".join(_student_row(s) for s in groups[grade])
        say(INDENT + f"{grade:<2s} --> [{rows}]")


def _partition(db):
    students = db.read_all()
    say(INDENT + "PASS/FAIL Partition", GREEN)
    fails = [s for s in students if not s.is_pass()]
    passes = [s for s in students if s.is_pass()]
    say(INDENT + f"FAIL --> [{', '.join(_student_row(s) for s in fails)}]")
    say(INDENT + f"PASS --> [{', '.join(_student_row(s) for s in passes)}]")


def _student_row(student):
    return (
        f"{student.name} :: {student.id} "
        f"--> GRADE: {student.overall_grade():>2s} "
        f"- MARK: {student.average_mark():.2f}"
    )


def _remove(db):
    sid = ask(INDENT + "Remove by ID: ").strip()
    if db.remove_by_id(sid):
        say(INDENT + f"Removing Student {sid} Account", YELLOW)
    else:
        say(INDENT + f"Student {sid} does not exist", RED)


def _clear(db):
    say(INDENT + "Clearing students database", YELLOW)
    answer = ask(
        INDENT + "Are you sure you want to clear the database (Y)ES/(N)O: ",
        RED,
    ).strip()
    if answer.upper() == "Y":
        db.clear()
        say(INDENT + "Students data cleared", YELLOW)
