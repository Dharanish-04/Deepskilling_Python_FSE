from courses.models import Department, Course, Student, Enrollment
from django.db.models import Count, F

cs_dept = Department.objects.create(name="Computer Science", head_of_dept="Dr. Rao", budget=500000)
math_dept = Department.objects.create(name="Mathematics", head_of_dept="Dr. Iyer", budget=300000)

c1 = Course.objects.create(name="Data Structures", code="CS101", credits=4, department=cs_dept)
c2 = Course.objects.create(name="Algorithms", code="CS102", credits=4, department=cs_dept)
c3 = Course.objects.create(name="Linear Algebra", code="MA101", credits=3, department=math_dept)
c4 = Course.objects.create(name="Calculus", code="MA102", credits=3, department=math_dept)

Student.objects.create(first_name="Aditi", last_name="Sharma", email="aditi@college.edu", department=cs_dept, enrollment_year=2023)
Student.objects.create(first_name="Rohan", last_name="Verma", email="rohan@college.edu", department=cs_dept, enrollment_year=2023)
Student.objects.create(first_name="Kiran", last_name="Patel", email="kiran@college.edu", department=math_dept, enrollment_year=2022)
Student.objects.create(first_name="Meera", last_name="Nair", email="meera@college.edu", department=math_dept, enrollment_year=2022)
Student.objects.create(first_name="Sanjay", last_name="Gupta", email="sanjay@college.edu", department=cs_dept, enrollment_year=2024)

cs_courses = Course.objects.filter(department__name="Computer Science")
print(list(cs_courses))

dept_counts = Department.objects.annotate(course_count=Count("course"))
for d in dept_counts:
    print(d.name, d.course_count)

from django.db import connection
students_with_dept = Student.objects.select_related("department").all()
for s in students_with_dept:
    print(s.first_name, s.department.name)
print(len(connection.queries))

Department.objects.update(budget=F("budget") * 1.1)
