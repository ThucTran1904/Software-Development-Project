# Software Development - University Application (CLI and GUI)

**Group 10 - Cmp15**
**Subject:** Software Development Studio 1
**Assessment:** Assessment 1 - Part 2 & Part 3

A university enrolment system delivered as two applications that share
the same data file:

- **CLIUniApp** - a command-line program where students can register,
  sign in, enrol in up to 4 subjects, change their password, and see
  their marks. Admins can list all students, group them by grade,
  partition into PASS/FAIL, remove a student, or clear the database.
- **GUIUniApp** - a Tkinter graphical version of the student flow
  (login, enrolment, subject view, exception handling).

Both applications read and write the same `students.data` file, so a
student registered on the CLI can log in on the GUI straight away, and
vice versa.

---

## Team

| Role        | Member                                       | Student ID | Part                               | Marks |
|-------------|----------------------------------------------|------------|------------------------------------|-------|
| Team Leader | Henry Thuc Tran                              | 26164741   | University System + Student System |  13   |
| Member 1    | David Esteban Barbosa Rodríguez              | 25012954   | Subject Enrolment System (CLI)     |  15   |
| Member 2    | Harikishan Siddapura Ravibabu                | 26224434   | Admin System (CLI)                 |  15   |
| Member 3    | Manisha Annaram                              | 26240806   | GUIUniApp (challenge)              |   7   |

Total: **50 marks** (Part 2) + 5 marks per person for the Part 3 showcase.

---

## How to run

You need **Python 3.8 or newer**. No external libraries - the CLI uses
only `re`, `pickle`, `os`, and `random` from the standard library, and
the GUI uses `tkinter`, which ships with Python. There is no
`pip install` step.

### CLIUniApp

From inside `CLIUniApp/`:

```
python main.py
```

or on Windows if `python` isn't on PATH:

```
py -3 main.py
```

### GUIUniApp

From inside `GUIUniApp/`:

```
python gui_main.py
```

or on Windows if `python` isn't on PATH:

```
py -3 gui_main.py
```

You can also launch either app from the repo root without `cd`:

```
py -3 .\CLIUniApp\main.py
py -3 .\GUIUniApp\gui_main.py
```

> **Windows tip:** if you see
> `Python was not found; run without arguments to install from the Microsoft Store...`,
> your PATH is pointing at the Store alias instead of a real
> interpreter. Use `py -3 ...` as shown above, or reinstall Python
> with the "Add Python to PATH" option ticked.

### Shared data file

`students.data` lives next to `CLIUniApp/database.py`, so the file
path is anchored to the module, not to your current working directory.
The GUI imports the same `Database` class and therefore reads and
writes the same file. The path always resolves to:

```
group10-Cmp15/CLIUniApp/students.data
```

You can launch the GUI from any working directory without it creating
a second empty file somewhere else. The first run auto-creates an
empty `students.data`.

---

## GUI windows

| Window            | Purpose                                                                                                              |
|-------------------|----------------------------------------------------------------------------------------------------------------------|
| Login window      | Main window. Reads `students.data`, validates the typed email + password.                                            |
| Enrolment window  | Opens after a successful login. Enrol in up to 4 subjects or jump to the Subject window.                             |
| Subject window    | Lists the student's enrolled subjects with mark and grade.                                                           |
| Exception window  | Pops up for empty fields, wrong email format, wrong password format, wrong credentials, or a 5th-subject attempt.    |

---

## Project layout

```
group10-Cmp15/
├── CLIUniApp/
│   ├── main.py                   University System (Henry)
│   ├── database.py               Shared file I/O (Henry - supports all)
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── student_controller.py Student login + register (Henry)
│   │   ├── subject_controller.py Course menu: enrol / remove / show / change pw (David)
│   │   └── admin_controller.py   Admin menu (Harikishan)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py            Student data class (Henry)
│   │   └── subject.py            Subject data class (Henry)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validators.py         Email + password regex (Henry)
│   └── students.data             Auto-created on first run
│
├── GUIUniApp/                    Challenge task (Manisha)
│   ├── gui_main.py               Entry window - launches login
│   └── windows/
│       ├── __init__.py
│       ├── login_window.py
│       ├── enrolment_window.py
│       ├── subject_window.py
│       └── exception_window.py
│
└── README.md                     This file
```

### Who owns what (mapped to the rubric)

| Area                                           | Member     | Marks |
|------------------------------------------------|------------|-------|
| University menu routing                        | Henry      | 4     |
| Student login + register + regex               | Henry      | 9     |
| Enrol / remove / view / change pw              | David      | 15    |
| Show / group / partition / remove / clear      | Harikishan | 15    |
| GUI: login / enrolment / subject / exception   | Manisha    | 7     |

Shared infrastructure (`database.py`, `models/`, `utils/`) was written
by Henry so every part reads and writes the file the same way.

---

## Rules the program enforces

### Email format

```
firstname.lastname@university.com
```

Regex: `^[a-zA-Z]+\.[a-zA-Z]+@university\.com$`

### Password format

- starts with one uppercase letter
- followed by at least 5 more letters (so 6+ letters total)
- ends with 3 or more digits

Example: `Helloworld123`. Regex:
`^[A-Z][A-Za-z]{5,}[0-9]{3,}$`

The `{5,}` matches the Sample I/O in the assessment PDF:
`Hello123` (5 letters) is rejected; `Helloworld123` (10 letters) is
accepted.

### Student ID

- 6 digits, zero-padded
- range `000001` - `999999`
- assigned randomly at registration

### Subject ID

- 3 digits, zero-padded
- range `001` - `999`
- assigned randomly at enrolment (unique within a student's list)

### Subject mark and grade

| Mark range | Grade |
|------------|-------|
| `< 50`     | Z     |
| `50 - 64`  | P     |
| `65 - 74`  | C     |
| `75 - 84`  | D     |
| `>= 85`    | HD    |

A student is **PASS** if their average mark across all enrolled
subjects is `>= 50`, otherwise **FAIL**.

### Limits

- a student can enrol in at most **4 subjects**
- a fresh subject gets a random mark between **25 and 100**

---

## How data is stored

All persistence goes through `database.py`. It pickles a list of plain
dicts into `students.data`. The first time the file is opened an empty
list is written, so the program never has to handle a
"file doesn't exist" error after the first run.

No controller reads or writes the file directly - they all call
`Database().read_all()`, `.add(...)`, `.update(...)`,
`.remove_by_id(...)`, or `.clear()`. This keeps the file format in one
place.

GUIUniApp imports the same `Database` class via a `sys.path` entry
added in `gui_main.py`, so there is no duplicated I/O code on the GUI
side.

If you want to wipe the database without deleting the file, use the
Admin menu "Clear database" option. If you want to reset it the quick
way, just delete `students.data` and re-run the program.

---

## Testing

There is no automated `pytest` suite - the program is smoke-tested by
hand. The core scenarios we checked:

### CLI

- [x] University menu routes between Admin and Student and exits on `X`
      with `Thank You`
- [x] Bad-format email/password is rejected with
      `Incorrect email or password format` and re-prompts
- [x] Valid-format login with no matching student prints
      `Student does not exist`
- [x] Valid-format register with an existing email prints
      `Student {Name} already exists`
- [x] Successful register prints `Name:` and `Enrolling Student`
      then returns to the Student menu
- [x] After login the student sees the Student Course Menu
- [x] Enrolment caps at 4 subjects and prints
      `Students are allowed to enrol in 4 subjects only`
- [x] `show` prints `Showing N subjects` with one line per subject
- [x] `change password` re-prompts on mismatch with
      `Password does not match - try again`
- [x] Admin `s` lists all students; prints
      `< Nothing to Display >` when empty
- [x] Admin `g` groups by grade in order Z/P/C/D/HD
- [x] Admin `p` partitions PASS/FAIL (average >= 50 rule)
- [x] Admin `r` reports `Removing Student {id} Account` or
      `Student {id} does not exist`
- [x] Admin `c` prompts for confirmation, wipes only on `Y`

### GUI

- [x] Login window refuses empty fields
- [x] Login window rejects bad email/password format via the
      Exception window
- [x] Login window rejects wrong credentials via the Exception window
- [x] Successful login opens the Enrolment window
- [x] Enrolment window blocks enrolment once at 4 subjects
- [x] Subject window lists enrolled subjects with marks and grades

---

## Known limitations / TODO

- No automated `pytest` suite - we rely on manual testing.
- Admin "remove by ID" does not prompt for a second confirmation.
- If the random 6-digit student ID collides with an existing
  student's ID (very unlikely), the second `.add()` still goes
  through; the brief doesn't require uniqueness on auto-generated
  IDs and all lookups are by email.

---

## Language choice

We agreed on **Python** as a team. Reasons:

1. Every member has used Python in earlier subjects, so there was no
   ramp-up cost and everyone could start coding their own part on
   day one.
2. The assessment's requirements (regex validation, file I/O,
   random-number generation, zero-padded IDs) all map directly onto
   Python's standard library, so we don't need any external packages
   and there is no `pip install` step for the tutor at showcase.
3. The GUI challenge is easy to build on top of `tkinter`, which
   ships with Python - no separate framework install and it runs on
   Windows, macOS, and Linux without changes.
4. Python's dict / list / pickle combo makes the shared
   `students.data` file trivial to read and write from both the CLI
   and GUI apps, without writing a custom parser.

### Recommended tooling for the team

- **Formatter:** `black` (run on save - keeps merge diffs small)
- **Linter:** `ruff` (catches unused imports before showcase)
- **Python version:** pin to `3.8+`
- **Editor:** VS Code with the official Python extension
- **Version control:** one shared Git repo; each member on their own
  branch, merged into `main` before the showcase
- **Branch hygiene:** don't commit `students.data` or `__pycache__/`
  (both are in `.gitignore`)

No third-party runtime dependencies, so there is no
`requirements.txt`. If you have Python 3.8+ installed, you can run the
program straight away.

---

## Attribution

All source code was written by the four members of Group 10 listed in
the team table above. Each member is responsible for their own
subsystem and will walk through their code at the Week 13 showcase.
