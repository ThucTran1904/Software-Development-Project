"""A small Toplevel used to surface errors: empty fields, bad email,
wrong credentials, or trying to enrol past the 4-subject cap.

Kept as its own class (rather than a tkinter messagebox) because the
marking rubric explicitly asks for four windows, one of which is the
exception window.
"""

import tkinter as tk


class ExceptionWindow(tk.Toplevel):
    def __init__(self, parent, message, title="Error"):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.configure(padx=20, pady=15)
        self.transient(parent)
        self.grab_set()

        tk.Label(
            self,
            text=message,
            fg="#b00020",
            font=("Segoe UI", 10, "bold"),
            wraplength=320,
            justify="left",
        ).pack(pady=(0, 10))

        tk.Button(self, text="OK", width=10, command=self.destroy).pack()

        self.bind("<Return>", lambda _e: self.destroy())
        self.focus_set()
