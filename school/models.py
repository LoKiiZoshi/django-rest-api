from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    established_date = models.DateField()

    def __str__(self):
        return self.name

class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.school.name})"

class Subject(models.Model):
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, related_name='students')
    date_of_birth = models.DateField()
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Parent of {self.student.user.first_name} {self.student.user.last_name}"

class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='exams')
    exam_date = models.DateField()
    total_marks = models.IntegerField()

    def __str__(self):
        return f"{self.subject.name} Exam on {self.exam_date}"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.IntegerField()
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.first_name}'s grade in {self.exam.subject.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.first_name} on {self.date}"