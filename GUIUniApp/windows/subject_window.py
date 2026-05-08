"""Subject window - lists the student's enrolled subjects with marks
and grades in a read-only table. Opened from the Enrolment window.
"""

import tkinter as tk
from tkinter import ttk


class SubjectWindow(tk.Toplevel):
    def __init__(self, parent, student):
        super().__init__(parent)
        self.title(f"GUIUniApp - Subjects ({student.name})")
        self.resizable(False, False)
        self.transient(parent)

        frame = ttk.Frame(self, padding=15)
        frame.pack()

        ttk.Label(
            frame, text="Enrolled Subjects", font=("Segoe UI", 13, "bold")
        ).pack(pady=(0, 10))

        columns = ("id", "mark", "grade")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=6)
        tree.heading("id", text="Subject ID")
        tree.heading("mark", text="Mark")
        tree.heading("grade", text="Grade")
        tree.column("id", width=100, anchor="center")
        tree.column("mark", width=80, anchor="center")
        tree.column("grade", width=80, anchor="center")

        for s in student.subjects:
            tree.insert("", "end", values=(s.id, s.mark, s.grade))

        tree.pack()

        if not student.subjects:
            ttk.Label(frame, text="No subjects enrolled yet.").pack(pady=(10, 0))

        ttk.Button(frame, text="Close", command=self.destroy).pack(pady=(15, 0))
