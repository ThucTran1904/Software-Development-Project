"""Subject model.

A subject has a 3-digit id, a random mark between 25 and 100, and a
grade derived from the mark. The grade thresholds are defined in the
assessment brief:

    mark < 50       -> Z  (Fail)
    50 <= mark < 65 -> P  (Pass)
    65 <= mark < 75 -> C  (Credit)
    75 <= mark < 85 -> D  (Distinction)
    mark >= 85      -> HD (High Distinction)
"""

import random


class Subject:
    def __init__(self, sid, mark=None, grade=None):
        self.id = sid
        self.mark = mark if mark is not None else random.randint(25, 100)
        self.grade = grade if grade is not None else Subject.grade_for(self.mark)

    def to_dict(self):
        return {"id": self.id, "mark": self.mark, "grade": self.grade}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["mark"], data["grade"])

    @staticmethod
    def grade_for(mark):
        if mark < 50:
            return "Z"
        if mark < 65:
            return "P"
        if mark < 75:
            return "C"
        if mark < 85:
            return "D"
        return "HD"

    @staticmethod
    def random_id():
        return f"{random.randint(1, 999):03d}"

    def __repr__(self):
        return f"Subject({self.id}, mark={self.mark}, grade={self.grade})"
