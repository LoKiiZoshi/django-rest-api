
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'enrollment_date', 'created_at', 'updated_at']
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))

class StudentCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Student
        fields = ['username', 'password', 'student_id', 'first_name', 'last_name', 
                 'email', 'phone', 'date_of_birth', 'gender', 'address', 'profile_image']
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        # Create student
        student = Student.objects.create(user=user, **validated_data)
        return student

class CourseSerializer(serializers.ModelSerializer):
    enrolled_students_count = serializers.SerializerMethodField()
    available_spots = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def get_enrolled_students_count(self, obj):
        return obj.enrollments.filter(status='enrolled').count()
    
    def get_available_spots(self, obj):
        enrolled_count = obj.enrollments.filter(status='enrolled').count()
        return max(0, obj.max_students - enrolled_count)

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['id', 'enrollment_date']

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']
    
    def validate(self, data):
        student = data['student']
        course = data['course']
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Student is already enrolled in this course")
        
        # Check course capacity
        enrolled_count = course.enrollments.filter(status='enrolled').count()
        if enrolled_count >= course.max_students:
            raise serializers.ValidationError("Course is full")
        
        # Check if course is active
        if not course.is_active:
            raise serializers.ValidationError("Course is not active")
        
        return data