from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_books_count(self, obj):
        return obj.books.count()

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    books_count = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = '__all__'
    
    def get_books_count(self, obj):
        return obj.books.count()
    
    def get_age(self, obj):
        if obj.birth_date:
            end_date = obj.death_date or date.today()
            return end_date.year - obj.birth_date.year
        return None

class PublisherSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Publisher
        fields = '__all__'
    
    def get_books_count(self, obj):
        return obj.books.count()

class BookSerializer(serializers.ModelSerializer):
    authors_names = serializers.SerializerMethodField()
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    library_name = serializers.CharField(source='library.name', read_only=True)
    availability_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def get_authors_names(self, obj):
        return [author.full_name for author in obj.authors.all()]
    
    def get_availability_status(self, obj):
        if obj.available_quantity > 0:
            return f"Available ({obj.available_quantity} copies)"
        return "Not Available"

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    library_name = serializers.CharField(source='library.name', read_only=True)
    is_membership_expired = serializers.ReadOnlyField()
    active_issues_count = serializers.SerializerMethodField()
    total_fines = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = '__all__'
    
    def get_active_issues_count(self, obj):
        return obj.book_issues.filter(status='ISSUED').count()
    
    def get_total_fines(self, obj):
        return obj.fines.filter(status='PENDING').aggregate(
            total=models.Sum('amount')
        )['total'] or 0

class BookIssueSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)
    returned_by_name = serializers.CharField(source='returned_by.get_full_name', read_only=True)
    days_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = BookIssue
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'

class FineSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    book_title = serializers.CharField(source='book_issue.book.title', read_only=True)
    waived_by_name = serializers.CharField(source='waived_by.get_full_name', read_only=True)
    
    class Meta:
        model = Fine
        fields = '__all__'
