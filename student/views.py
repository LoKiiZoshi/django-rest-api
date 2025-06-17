from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Student, Course, Enrollment
from .serializers import (
    StudentSerializer, StudentCreateSerializer,
    CourseSerializer, EnrollmentSerializer, EnrollmentCreateSerializer
)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'gender']
    search_fields = ['first_name', 'last_name', 'student_id', 'email']
    ordering_fields = ['created_at', 'first_name', 'last_name', 'enrollment_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get all enrollments for a specific student"""
        student = self.get_object()
        enrollments = student.enrollments.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll student in a course"""
        student = self.get_object()
        course_id = request.data.get('course_id')
        
        if not course_id:
            return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EnrollmentCreateSerializer(data={'student': student.id, 'course': course.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get student statistics"""
        total_students = Student.objects.count()
        active_students = Student.objects.filter(status='active').count()
        graduated_students = Student.objects.filter(status='graduated').count()
        
        stats = {
            'total_students': total_students,
            'active_students': active_students,
            'graduated_students': graduated_students,
            'inactive_students': total_students - active_students - graduated_students,
        }
        return Response(stats)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty', 'is_active']
    search_fields = ['name', 'code', 'instructor']
    ordering_fields = ['created_at', 'name', 'code', 'credits']
    ordering = ['code']
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students enrolled in a specific course"""
        course = self.get_object()
        enrollments = course.enrollments.filter(status='enrolled')
        students = [enrollment.student for enrollment in enrollments]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular courses by enrollment count"""
        courses = Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).filter(is_active=True).order_by('-enrollment_count')[:10]
        
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'grade']
    ordering_fields = ['enrollment_date', 'completion_date']
    ordering = ['-enrollment_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        return EnrollmentSerializer
    
    @action(detail=True, methods=['patch'])
    def update_grade(self, request, pk=None):
        """Update grade for an enrollment"""
        enrollment = self.get_object()
        grade = request.data.get('grade')
        
        if not grade:
            return Response({'error': 'Grade is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        enrollment.grade = grade
        if grade not in ['I', 'W']:  # Not incomplete or withdrawn
            enrollment.status = 'completed'
            if not enrollment.completion_date:
                from datetime import date
                enrollment.completion_date = date.today()
        
        enrollment.save()
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get enrollments filtered by student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        enrollments = self.queryset.filter(student__id=student_id)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)