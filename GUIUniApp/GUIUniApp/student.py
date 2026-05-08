class Student:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.subjects = []

    def enrol(self, subject):
        if len(self.subjects) >= 4:
            return False
        self.subjects.append(subject)
        return True