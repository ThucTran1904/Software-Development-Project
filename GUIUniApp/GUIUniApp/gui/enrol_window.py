import tkinter as tk
from tkinter import messagebox
from subject import Subject
from database import save_students, load_students
from gui.subject_window import open_subject_window

def open_enrol_window(student):
    root = tk.Tk()
    root.title("Enrolment")

    def enrol():
        if len(student.subjects) >= 4:
            messagebox.showerror("Error", "Max 4 subjects allowed")
            return

        subject = Subject()
        student.subjects.append(subject)

        students = load_students()

        # update the correct student
        for i in range(len(students)):
            if students[i].email == student.email:
                students[i] = student

        save_students(students)

        messagebox.showinfo("Success", f"Enrolled in subject {subject.id}")

    

    def show_subjects():
        open_subject_window(student)

    tk.Button(root, text="Enrol Subject", command=enrol).pack()
    tk.Button(root, text="Show Subjects", command=show_subjects).pack()

    root.mainloop()