# Parent Class 1
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_person_info(self):
        print("----- Person Info -----")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")

# Parent Class 2
class Student:
    def __init__(self, student_id, major):
        self.student_id = student_id
        self.major = major

    def display_student_info(self):
        print("----- Student Info -----")
        print(f"Student ID: {self.student_id}")
        print(f"Major: {self.major}")

# Child Class - Inheriting from both Person and Student
class CollegeStudent(Person, Student):
    def __init__(self, name, age, student_id, major, college_name):
        # Initialize attributes from both parent classes
        Person.__init__(self, name, age)
        Student.__init__(self, student_id, major)
        self.college_name = college_name

    def display_college_student_info(self):
        print("===== College Student Details =====")
        self.display_person_info()
        self.display_student_info()
        print(f"College: {self.college_name}")

# Creating an object of CollegeStudent
student1 = CollegeStudent(
    name="Sahil",
    age=21,
    student_id="VIT123456",
    major="Computer Science",
    college_name="VIT Vellore"
)

# Calling method to display all details
student1.display_college_student_info()

