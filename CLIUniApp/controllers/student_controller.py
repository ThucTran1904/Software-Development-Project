"""Student System menu - login, register, and exit.

On successful login we hand control to the Subject Enrolment System
(subject_controller). On a successful register we just go back to the
student menu - the brief does not auto-login newly-registered students.

All printed strings are indented to match the Sample I/O in the
assessment PDF. The student menu sits one level under the University
menu, so every line here is prefixed with 8 spaces.
"""

import random

from database import Database
from models.student import Student
from utils.validators import is_valid_email, is_valid_password, name_from_email
from utils.term import say, ask, GREEN, YELLOW, RED
from controllers import subject_controller


INDENT = " " * 8
MENU_PROMPT = INDENT + "Student System (l/r/x): "


def run():
    db = Database()
    while True:
        choice = ask(MENU_PROMPT, GREEN).strip().lower()
        if choice == "l":
            _login(db)
        elif choice == "r":
            _register(db)
        elif choice == "x":
            return
        # anything else: fall through and re-prompt (matches sample)


def _prompt_credentials():
    """Prompt for email + password in a loop until both formats pass."""
    while True:
        email = ask(INDENT + "Email: ")
        password = ask(INDENT + "Password: ")
        if is_valid_email(email) and is_valid_password(password):
            say(INDENT + "email and password formats acceptable", YELLOW)
            return email, password
        say(INDENT + "Incorrect email or password format", RED)


def _login(db):
    say(INDENT + "Student Sign In", GREEN)
    email, password = _prompt_credentials()

    student = db.find_by_email(email)
    if student is None or student.password != password:
        say(INDENT + "Student does not exist", RED)
        return

    subject_controller.run(db, student)


def _register(db):
    say(INDENT + "Student Sign Up", GREEN)
    email, password = _prompt_credentials()

    name = name_from_email(email)
    if db.find_by_email(email) is not None:
        say(INDENT + f"Student {name} already exists", RED)
        return

    say(INDENT + f"Name: {name}")
    say(INDENT + f"Enrolling Student {name}", YELLOW)
    sid = f"{random.randint(1, 999999):06d}"
    db.add(Student(sid, name, email, password))
