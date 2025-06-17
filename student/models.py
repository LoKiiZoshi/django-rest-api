from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    profile_image = models.ImageField(upload_to='students/profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    instructor = models.CharField(max_length=100)
    max_students = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D+', 'D+'), ('D', 'D'), ('F', 'F'),
        ('I', 'Incomplete'), ('W', 'Withdrawn')
    ]
    
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('failed', 'Failed')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.course.code}"