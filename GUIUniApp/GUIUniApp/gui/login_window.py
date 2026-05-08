import tkinter as tk
from tkinter import messagebox
from database import load_students
from gui.enrol_window import open_enrol_window

def open_login_window():
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="University Login", font=("Arial", 16)).pack()

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Password").pack()
    pass_entry = tk.Entry(root, show="*")
    pass_entry.pack()

    def login():
        email = email_entry.get()
        password = pass_entry.get()

        # Exception: empty fields
        if not email or not password:
            messagebox.showerror("Error", "Fields cannot be empty")
            return

        students = load_students()

        for s in students:
            if s.email == email and s.password == password:
                root.destroy()
                open_enrol_window(s)
                return

        # Exception: wrong credentials
        messagebox.showerror("Error", "Invalid credentials")

    tk.Button(root, text="Login", command=login).pack()

    root.mainloop()