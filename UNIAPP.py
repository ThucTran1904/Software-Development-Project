import random

DATA_FILE = "students.data"


# ---- SUBJECT CLASS ----
class Subject:
    def __init__(self):
        self.id = random.randint(1, 999)
        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.mark < 50:
            return "Z"
        elif self.mark < 65:
            return "P"
        elif self.mark < 75:
            return "C"
        elif self.mark < 85:
            return "D"
        else:
            return "HD"

    def display(self):
        print(f"[ Subject::{str(self.id).zfill(3)} -- mark = {self.mark} -- grade = {self.grade:>3} ]")


# ---- STUDENT CLASS ----
class Student:
    def __init__(self, name, email, password):
        self.id = random.randint(1, 999999)
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def get_average(self):
        if len(self.subjects) == 0:
            return 0
        total = 0
        for s in self.subjects:
            total = total + s.mark
        return total / len(self.subjects)

    def get_grade(self):
        avg = self.get_average()
        if avg < 50:
            return "Z"
        elif avg < 65:
            return "P"
        elif avg < 75:
            return "C"
        elif avg < 85:
            return "D"
        else:
            return "HD"

    def is_pass(self):
        if self.get_average() >= 50:
            return True
        return False


# ---- FILE FUNCTIONS ----
# we save students as text lines in students.data
# format: id,name,email,password,subjectid-mark-grade,subjectid-mark-grade,...

def save_students(students):
    f = open(DATA_FILE, "w")
    for s in students:
        # build the subject part
        subject_data = ""
        for sub in s.subjects:
            subject_data = subject_data + str(sub.id) + "-" + str(sub.mark) + "-" + sub.grade + ";"
        # write one line per student
        line = str(s.id) + "," + s.name + "," + s.email + "," + s.password + "," + subject_data
        f.write(line + "\n")
    f.close()


def load_students():
    students = []
    # if file doesnt exist just return empty list
    try:
        f = open(DATA_FILE, "r")
        lines = f.readlines()
        f.close()
    except:
        return students

    for line in lines:
        line = line.strip()
        if line == "":
            continue
        parts = line.split(",")
        # parts: 0=id, 1=name, 2=email, 3=password, 4=subjects
        s = Student(parts[1], parts[2], parts[3])
        s.id = int(parts[0])
        # load subjects if any
        if len(parts) > 4 and parts[4] != "":
            subject_entries = parts[4].split(";")
            for entry in subject_entries:
                if entry == "":
                    continue
                sub_parts = entry.split("-")
                sub = Subject.__new__(Subject)
                sub.id = int(sub_parts[0])
                sub.mark = int(sub_parts[1])
                sub.grade = sub_parts[2]
                s.subjects.append(sub)
        students.append(s)
    return students


def find_by_email(students, email):
    for s in students:
        if s.email == email:
            return s
    return None


def find_by_id(students, sid):
    for s in students:
        if s.id == sid:
            return s
    return None


# ---- EMAIL AND PASSWORD CHECK ----
def check_email(email):
    # must have exactly one @ and end with @university.com
    if "@" not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    if parts[1] != "university.com":
        return False
    # must have a dot in the name part like john.smith
    if "." not in parts[0]:
        return False
    return True


def check_password(password):
    # must start with uppercase
    if len(password) == 0:
        return False
    if password[0].isupper() == False:
        return False
    # count letters and digits
    letter_count = 0
    digit_count = 0
    for c in password:
        if c.isalpha():
            letter_count = letter_count + 1
        if c.isdigit():
            digit_count = digit_count + 1
    # need at least 5 letters and 3 digits
    if letter_count < 5:
        return False
    if digit_count < 3:
        return False
    return True


# ---- SUBJECT ENROLMENT MENU ----
def subject_menu(student):
    while True:
        choice = input("        Student Course Menu (c/e/r/s/x): ").strip().lower()

        if choice == "e":
            # enrol in a subject
            if len(student.subjects) >= 4:
                print("Students are allowed to enrol in 4 subjects only")
            else:
                new_subject = Subject()
                student.subjects.append(new_subject)
                # save updated student
                all_students = load_students()
                for i in range(len(all_students)):
                    if all_students[i].id == student.id:
                        all_students[i] = student
                save_students(all_students)
                print(f"Enrolling in Subject-{str(new_subject.id).zfill(3)}")
                print(f"You are now enrolled in {len(student.subjects)} out of 4 subjects")

        elif choice == "r":
            # remove a subject
            if len(student.subjects) == 0:
                print("< Nothing to Display >")
            else:
                sid = input("Remove Subject by ID: ").strip()
                found = False
                for s in student.subjects:
                    if str(s.id).zfill(3) == sid or str(s.id) == sid:
                        student.subjects.remove(s)
                        found = True
                        break
                if found:
                    all_students = load_students()
                    for i in range(len(all_students)):
                        if all_students[i].id == student.id:
                            all_students[i] = student
                    save_students(all_students)
                    print(f"Droping Subject-{sid}")
                    print(f"You are now enrolled in {len(student.subjects)} out of 4 subjects")
                else:
                    print(f"Subject {sid} not found")

        elif choice == "s":
            # show all subjects
            print(f"Showing {len(student.subjects)} subjects")
            for s in student.subjects:
                s.display()

        elif choice == "c":
            # change password
            print("Updating Password")
            new_pass = input("New Password: ").strip()
            confirm = input("Confirm Password: ").strip()
            if new_pass != confirm:
                print("Password does not match - try again")
            elif check_password(new_pass) == False:
                print("Incorrect password format")
            else:
                student.password = new_pass
                all_students = load_students()
                for i in range(len(all_students)):
                    if all_students[i].id == student.id:
                        all_students[i] = student
                save_students(all_students)

        elif choice == "x":
            break
        else:
            print("Invalid option")


# ---- STUDENT MENU ----
def student_menu():
    while True:
        choice = input("        Student System (l/r/x): ").strip().lower()

        if choice == "r":
            # register
            print("Student Sign Up")
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if check_email(email) == False or check_password(password) == False:
                print("        Incorrect email or password format")
                continue

            print("        email and password formats acceptable")

            all_students = load_students()
            existing = find_by_email(all_students, email)
            if existing != None:
                print(f"        Student {existing.name} already exists")
                continue

            # get name from email
            name_part = email.split("@")[0]
            name_bits = name_part.split(".")
            name = ""
            for bit in name_bits:
                name = name + bit.capitalize() + " "
            name = name.strip()

            print(f"        Name: {name}")
            new_student = Student(name, email, password)
            all_students.append(new_student)
            save_students(all_students)
            print(f"        Enrolling Student {name}")

        elif choice == "l":
            # login
            print("Student Sign In")
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if check_email(email) == False or check_password(password) == False:
                print("        Incorrect email or password format")
                continue

            print("        email and password formats acceptable")

            all_students = load_students()
            student = find_by_email(all_students, email)

            if student == None:
                print("        Student does not exist")
                continue

            if student.password != password:
                print("        Incorrect password")
                continue

            subject_menu(student)

        elif choice == "x":
            break
        else:
            print("        Invalid option")


# ---- ADMIN MENU ----
def admin_menu():
    while True:
        choice = input("        Admin System (c/g/p/r/s/x): ").strip().lower()

        if choice == "s":
            # show all students
            print("        Student List")
            all_students = load_students()
            if len(all_students) == 0:
                print("        < Nothing to Display >")
            else:
                for s in all_students:
                    print(f"        {s.name} :: {str(s.id).zfill(6)} --> Email: {s.email}")

        elif choice == "g":
            # group by grade
            print("        Grade Grouping")
            all_students = load_students()
            if len(all_students) == 0:
                print("        < Nothing to Display >")
            else:
                # go through each grade and find matching students
                for grade in ["Z", "P", "C", "D", "HD"]:
                    group = []
                    for s in all_students:
                        if s.get_grade() == grade:
                            avg = round(s.get_average(), 2)
                            group.append(f"{s.name} :: {str(s.id).zfill(6)} --> GRADE: {grade:>2} - MARK: {avg}")
                    if len(group) > 0:
                        print(f"        {grade}  --> [{', '.join(group)}]")

        elif choice == "p":
            # partition pass fail
            print("        PASS/FAIL Partition")
            all_students = load_students()
            pass_list = []
            fail_list = []
            for s in all_students:
                avg = round(s.get_average(), 2)
                grade = s.get_grade()
                info = f"{s.name} :: {str(s.id).zfill(6)} --> GRADE: {grade:>2} - MARK: {avg}"
                if s.is_pass():
                    pass_list.append(info)
                else:
                    fail_list.append(info)
            print(f"        FAIL --> [{', '.join(fail_list)}]")
            print(f"        PASS --> [{', '.join(pass_list)}]")

        elif choice == "r":
            # remove a student
            sid = input("        Remove by ID: ").strip()
            all_students = load_students()
            found = False
            new_list = []
            for s in all_students:
                if str(s.id).zfill(6) == sid or str(s.id) == sid:
                    found = True
                else:
                    new_list.append(s)
            if found:
                save_students(new_list)
                print(f"        Removing Student {sid} Account")
            else:
                print(f"        Student {sid} does not exist")

        elif choice == "c":
            # clear all students
            print("        Clearing students database")
            answer = input("        Are you sure you want to clear the database (Y)ES/(N)O: ").strip().upper()
            if answer == "Y":
                save_students([])
                print("        Students data cleared")

        elif choice == "x":
            break
        else:
            print("        Invalid option")


# ---- MAIN ----
def main():
    while True:
        choice = input("University System: (A)dmin, (S)tudent, or X : ").strip().upper()
        if choice == "A":
            admin_menu()
        elif choice == "S":
            student_menu()
        elif choice == "X":
            print("Thank You")
            break
        else:
            print("Invalid option")


main()
