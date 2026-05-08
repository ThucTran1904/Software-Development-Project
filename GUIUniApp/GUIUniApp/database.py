import pickle
import os

FILE = "students.data"

def load_students():
    if not os.path.exists(FILE):
        return []
    
    with open(FILE, "rb") as f:
        try:
            return pickle.load(f)
        except:
            return []

def save_students(students):
    with open(FILE, "wb") as f:
        pickle.dump(students, f)