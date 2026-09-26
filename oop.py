class Student:
    no_of_students = 0

    def __init__(self, name, age=0, courses=None):
        self.name = name
        self.age = age
        self.courses = courses
        Student.no_of_students += 1

    def descreibe(self):
        print(f"My Name is : {self.name}, Age: {self.age}, Courses: {self.courses}")


student_1 = Student("John", 20, ["Math", "Science"])
student_2 = Student("Alice", 22, ["English", "History"])

student_1.descreibe()