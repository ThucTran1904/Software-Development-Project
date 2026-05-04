"""Email and password validators plus a small name-from-email helper.

Email rule from the brief:
    firstname.lastname@university.com

Password rule from the brief:
    (i)   starts with an upper-case character
    (ii)  contains at least five (5) more letters after the first one
    (iii) is followed by three (3) or more digits

The sample I/O in the assessment PDF rejects "Hello123" and accepts
"Helloworld123", which is why the middle group is {5,} (not {4,}).
"""

import re


EMAIL_PATTERN = re.compile(r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$")
PASSWORD_PATTERN = re.compile(r"^[A-Z][A-Za-z]{5,}[0-9]{3,}$")


def is_valid_email(email):
    return bool(EMAIL_PATTERN.match(email))


def is_valid_password(password):
    return bool(PASSWORD_PATTERN.match(password))


def name_from_email(email):
    """Turn 'john.smith@university.com' into 'John Smith'."""
    local = email.split("@", 1)[0]
    first, _, last = local.partition(".")
    return f"{first.capitalize()} {last.capitalize()}"
