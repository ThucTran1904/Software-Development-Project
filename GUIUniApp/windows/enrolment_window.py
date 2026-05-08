"""Enrolment window - opens after a successful login.

The student can enrol in up to four subjects and jump across to the
Subject window to review what they have. Attempting a fifth enrolment
pops up an ExceptionWindow, matching the brief.
"""

import tkinter as tk
from tkinter import ttk

from models.subject import Subject

from windows.exception_window import ExceptionWindow
from windows.subject_window import SubjectWindow


MAX_SUBJECTS = 4


class EnrolmentWindow(tk.Toplevel):
    def __init__(self, parent, db, student, on_close=None):
        super().__init__(parent)
        self.db = db
        self.student = student
        self._on_close = on_close

        self.title(f"GUIUniApp - Enrolment ({student.name})")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._logout)

        frame = ttk.Frame(self, padding=20)
        frame.pack()

        ttk.Label(
            frame, text=f"Welcome, {student.name}", font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 5))

        ttk.Label(frame, text=f"Student ID: {student.id}").grid(
            row=1, column=0, columnspan=2, pady=(0, 15)
        )

        self.status_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.status_var, font=("Segoe UI", 10)).grid(
            row=2, column=0, columnspan=2, pady=(0, 10)
        )

        ttk.Button(frame, text="Enrol in a new subject", command=self._enrol, width=28).grid(
            row=3, column=0, columnspan=2, pady=4, sticky="ew"
        )
        ttk.Button(frame, text="View my subjects", command=self._view_subjects, width=28).grid(
            row=4, column=0, columnspan=2, pady=4, sticky="ew"
        )
        ttk.Button(frame, text="Logout", command=self._logout, width=28).grid(
            row=5, column=0, columnspan=2, pady=(10, 0), sticky="ew"
        )

        self._refresh_status()

    def _refresh_status(self):
        self.status_var.set(
            f"Enrolled in {len(self.student.subjects)} out of {MAX_SUBJECTS} subjects"
        )

    def _enrol(self):
        if len(self.student.subjects) >= MAX_SUBJECTS:
            ExceptionWindow(self, "Students are allowed to enrol in 4 subjects only.")
            return

        taken = {s.id for s in self.student.subjects}
        sid = Subject.random_id()
        while sid in taken:
            sid = Subject.random_id()

        subject = Subject(sid)
        self.student.subjects.append(subject)
        self.db.update(self.student)
        self._refresh_status()

        ExceptionWindow(
            self,
            f"Enrolled in Subject-{int(subject.id)}\n"
            f"Mark: {subject.mark}   Grade: {subject.grade}",
            title="Enrolment successful",
        )

    def _view_subjects(self):
        SubjectWindow(self, self.student)

    def _logout(self):
        self.destroy()
        if self._on_close:
            self._on_close()
