"""Login window - the main window of GUIUniApp.

Reads Student objects from the shared students.data and validates
the typed email / password against them. Empty fields, wrong format,
and wrong credentials all route to the ExceptionWindow.
"""

import tkinter as tk
from tkinter import ttk

from database import Database
from utils.validators import is_valid_email, is_valid_password

from windows.exception_window import ExceptionWindow
from windows.enrolment_window import EnrolmentWindow


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.db = Database()

        root.title("GUIUniApp - Login")
        root.resizable(False, False)

        frame = ttk.Frame(root, padding=20)
        frame.pack()

        ttk.Label(frame, text="GUIUniApp", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=32).grid(
            row=1, column=1, pady=5
        )

        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=32).grid(
            row=2, column=1, pady=5
        )

        ttk.Button(frame, text="Login", command=self._login).grid(
            row=3, column=0, columnspan=2, pady=(15, 0), sticky="ew"
        )

        root.bind("<Return>", lambda _e: self._login())

    def _login(self):
        email = self.email_var.get().strip()
        password = self.password_var.get()

        if not email or not password:
            ExceptionWindow(self.root, "Email and password fields cannot be empty.")
            return

        if not is_valid_email(email):
            ExceptionWindow(
                self.root,
                "Incorrect email format.\nExpected firstname.lastname@university.com",
            )
            return

        if not is_valid_password(password):
            ExceptionWindow(
                self.root,
                "Incorrect password format.\nMust start with an upper-case letter,"
                " contain 6+ letters, and end with 3+ digits.",
            )
            return

        student = self.db.find_by_email(email)
        if student is None or student.password != password:
            ExceptionWindow(self.root, "Student does not exist.")
            return

        # clear fields for any future return to this window
        self.email_var.set("")
        self.password_var.set("")
        self.root.withdraw()

        EnrolmentWindow(self.root, self.db, student, on_close=self._on_logout)

    def _on_logout(self):
        self.root.deiconify()
