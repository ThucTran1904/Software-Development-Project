import tkinter as tk

def open_subject_window(student):
    win = tk.Toplevel()
    win.title("Subjects")

    for sub in student.subjects:
        text = f"ID: {sub.id} | Mark: {sub.mark} | Grade: {sub.grade}"
        tk.Label(win, text=text).pack()