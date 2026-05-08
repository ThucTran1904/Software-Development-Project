"""Subject Enrolment System - the menu a logged-in student sees.

Four actions plus exit: change password, enrol, remove, show. All
prompts sit two levels deep in the PDF sample (University -> Student
System -> Course Menu), so every printed line uses a 16-space indent.
"""

from models.subject import Subject
from utils.validators import is_valid_password
from utils.term import say, ask, GREEN, YELLOW, RED


INDENT = " " * 16
MENU_PROMPT = INDENT + "Student Course Menu (c/e/r/s/x): "
MAX_SUBJECTS = 4


def run(db, student):
    while True:
        choice = ask(MENU_PROMPT, GREEN).strip().lower()
        if choice == "c":
            _change_password(db, student)
        elif choice == "e":
            _enrol(db, student)
        elif choice == "r":
            _remove(db, student)
        elif choice == "s":
            _show(student)
        elif choice == "x":
            return


def _change_password(db, student):
    say(INDENT + "Updating Password", YELLOW)
    while True:
        new_pw = ask(INDENT + "New Password: ")
        if is_valid_password(new_pw):
            break
        say(INDENT + "Incorrect password format", RED)
    while True:
        confirm = ask(INDENT + "Confirm Password: ")
        if confirm == new_pw:
            break
        say(INDENT + "Password does not match - try again", RED)
    student.password = new_pw
    db.update(student)


def _enrol(db, student):
    if len(student.subjects) >= MAX_SUBJECTS:
        say(INDENT + "Students are allowed to enrol in 4 subjects only", RED)
        return

    taken = {s.id for s in student.subjects}
    sid = Subject.random_id()
    while sid in taken:
        sid = Subject.random_id()

    subject = Subject(sid)
    student.subjects.append(subject)
    say(INDENT + f"Enrolling in Subject-{int(sid)}", YELLOW)
    say(INDENT + f"You are now enrolled in {len(student.subjects)} out of {MAX_SUBJECTS} subjects", YELLOW)
    db.update(student)


def _remove(db, student):
    sid = ask(INDENT + "Remove Subject by ID: ").strip()
    if sid.isdigit():
        sid = sid.zfill(3)

    match = next((s for s in student.subjects if s.id == sid), None)
    if match is None:
        say(INDENT + f"Subject {sid} does not exist", RED)
        return

    student.subjects.remove(match)
    say(INDENT + f"Dropping Subject-{int(match.id)}", YELLOW)
    say(INDENT + f"You are now enrolled in {len(student.subjects)} out of {MAX_SUBJECTS} subjects", YELLOW)
    db.update(student)


def _show(student):
    count = len(student.subjects)
    say(INDENT + f"Showing {count} subjects", YELLOW)
    for s in student.subjects:
        say(INDENT + f"[ Subject::{s.id} -- mark = {s.mark} -- grade = {s.grade:>3s} ]")
