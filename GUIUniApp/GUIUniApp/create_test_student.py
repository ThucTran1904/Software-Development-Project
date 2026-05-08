from student import Student
from database import save_students

s = Student("test@university.com", "Password123")

save_students([s])

print("Test student created!")