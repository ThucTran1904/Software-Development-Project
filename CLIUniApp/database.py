"""Pickle-backed storage for Student objects.

All CRUD goes through this class. Controllers never open the file
themselves, so the file format lives in one place. Storing plain
dicts (via Student.to_dict) keeps the pickle file portable across
versions of the Student class.

The data file sits next to this module so the CLI and GUI apps share
the same students.data regardless of which working directory the user
launches them from.
"""

import os
import pickle

from models.student import Student


_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.data")


class Database:
    def __init__(self, path=None):
        self.path = path or _DEFAULT_PATH
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.path):
            with open(self.path, "wb") as f:
                pickle.dump([], f)

    def _load(self):
        with open(self.path, "rb") as f:
            raw = pickle.load(f)
        return [Student.from_dict(d) for d in raw]

    def _save(self, students):
        with open(self.path, "wb") as f:
            pickle.dump([s.to_dict() for s in students], f)

    def read_all(self):
        return self._load()

    def add(self, student):
        students = self._load()
        students.append(student)
        self._save(students)

    def update(self, student):
        students = self._load()
        for i, s in enumerate(students):
            if s.id == student.id:
                students[i] = student
                break
        else:
            students.append(student)
        self._save(students)

    def remove_by_id(self, sid):
        students = self._load()
        remaining = [s for s in students if s.id != sid]
        if len(remaining) == len(students):
            return False
        self._save(remaining)
        return True

    def find_by_email(self, email):
        for s in self._load():
            if s.email == email:
                return s
        return None

    def find_by_id(self, sid):
        for s in self._load():
            if s.id == sid:
                return s
        return None

    def clear(self):
        self._save([])
