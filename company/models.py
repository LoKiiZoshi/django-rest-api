from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='projects')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='tasks')
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Client(models.Model):
    name = models.CharField(max_length=100) 
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # Fixed invalid field name
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name
    

class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True)
    created_at = models.DateTimeField(max_length=100)
    total_staff = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name 
    
    
    
    
    
class CompanyBlog(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

 
    
class MediaUpload(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/images/', blank=True, null=True)
    video = models.FileField(upload_to='uploads/videos/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.title
    
    


class EmployeeReview(models.Model):
    REVIEW_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    review_date = models.DateField(default=timezone.now)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    performance = models.CharField(max_length=20, choices=REVIEW_CHOICES, default='average')
    comments = models.TextField(blank=True)
    document = models.FileField(upload_to='uploads/reviews/', blank=True, null=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.employee.first_name} by {self.reviewer_name}"


    
    
    

