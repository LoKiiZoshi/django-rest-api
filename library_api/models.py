from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta

class Library(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    established_date = models.DateField()
    librarian = models.CharField(max_length=100)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    total_books = models.IntegerField(default=0)
    total_members = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Libraries'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['first_name', 'last_name']

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Book(models.Model):
    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
        ('DAMAGED', 'Damaged'),
    ]

    title = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, unique=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()
    pages = models.IntegerField(validators=[MinValueValidator(1)])
    language = models.CharField(max_length=50, default='English')
    edition = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='GOOD')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    available_quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    shelf_location = models.CharField(max_length=50, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.available_quantity == 0:
            self.is_available = False
        else:
            self.is_available = True
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']

class Member(models.Model):
    MEMBERSHIP_TYPES = [
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
        ('STAFF', 'Staff'),
        ('PUBLIC', 'Public'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPES)
    membership_date = models.DateField(auto_now_add=True)
    membership_expiry = models.DateField()
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='members')
    profile_picture = models.ImageField(upload_to='members/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    max_books_allowed = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.member_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_membership_expired(self):
        return date.today() > self.membership_expiry

    def save(self, *args, **kwargs):
        if not self.membership_expiry:
            self.membership_expiry = date.today() + timedelta(days=365)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['first_name', 'last_name']

class BookIssue(models.Model):
    STATUS_CHOICES = [
        ('ISSUED', 'Issued'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_issues')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='book_issues')
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ISSUED')
    renewal_count = models.IntegerField(default=0)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_books')
    returned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='returned_books', null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} - {self.member.full_name}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = date.today() + timedelta(days=14)  # 2 weeks default
        
        # Check if overdue
        if self.status == 'ISSUED' and date.today() > self.due_date:
            self.status = 'OVERDUE'
            
        super().save(*args, **kwargs)

    @property
    def days_overdue(self):
        if self.status in ['ISSUED', 'OVERDUE'] and date.today() > self.due_date:
            return (date.today() - self.due_date).days
        return 0

    class Meta:
        ordering = ['-issued_date']

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('FULFILLED', 'Fulfilled'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    fulfilled_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} reserved by {self.member.full_name}"

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = date.today() + timedelta(days=7)  # 1 week reservation
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-reservation_date']
        unique_together = ['book', 'member']

class Fine(models.Model):
    FINE_TYPES = [
        ('OVERDUE', 'Overdue'),
        ('DAMAGE', 'Damage'),
        ('LOST', 'Lost Book'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('WAIVED', 'Waived'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='fines')
    book_issue = models.ForeignKey(BookIssue, on_delete=models.CASCADE, related_name='fines', null=True, blank=True)
    fine_type = models.CharField(max_length=10, choices=FINE_TYPES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    fine_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    paid_date = models.DateField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    waived_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fine for {self.member.full_name} - ${self.amount}"

    class Meta:
        ordering = ['-fine_date']