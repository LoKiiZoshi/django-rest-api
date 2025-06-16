from rest_framework import generics
from .models import School, Classroom, Subject, Teacher, Student, Parent, Exam, Grade, Attendance
from .serializers import (SchoolSerializer, ClassroomSerializer, SubjectSerializer, 
                         TeacherSerializer, StudentSerializer, ParentSerializer, 
                         ExamSerializer, GradeSerializer, AttendanceSerializer)

# School APIs
class SchoolListCreateView(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class SchoolDetailView(generics.RetrieveUpdateDestroyAPIView):  
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

# Classroom APIs
class ClassroomListCreateView(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class ClassroomBySchoolView(generics.ListAPIView):
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Classroom.objects.filter(school_id=school_id)

# Subject APIs
class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectBySchoolView(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Subject.objects.filter(school_id=school_id)

# Teacher APIs
class TeacherListCreateView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeacherBySchoolView(generics.ListAPIView):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Teacher.objects.filter(school_id=school_id)

# Student APIs
class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentBySchoolView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Student.objects.filter(school_id=school_id)

class StudentByClassroomView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        classroom_id = self.kwargs['classroom_id']
        return Student.objects.filter(classroom_id=classroom_id)

# Parent APIs
class ParentListCreateView(generics.ListCreateAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class ParentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class ParentByStudentView(generics.ListAPIView):
    serializer_class = ParentSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Parent.objects.filter(student_id=student_id)

# Exam APIs
class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamByClassroomView(generics.ListAPIView):
    serializer_class = ExamSerializer

    def get_queryset(self):
        classroom_id = self.kwargs['classroom_id']
        return Exam.objects.filter(classroom_id=classroom_id)

class ExamBySubjectView(generics.ListAPIView):
    serializer_class = ExamSerializer

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Exam.objects.filter(subject_id=subject_id)

# Grade APIs
class GradeListCreateView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class GradeByStudentView(generics.ListAPIView):
    serializer_class = GradeSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Grade.objects.filter(student_id=student_id)

class GradeByExamView(generics.ListAPIView):
    serializer_class = GradeSerializer

    def get_queryset(self):
        exam_id = self.kwargs['exam_id']
        return Grade.objects.filter(exam_id=exam_id)

# Attendance APIs
class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceByStudentView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Attendance.objects.filter(student_id=student_id)

class AttendanceByDateView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        return Attendance.objects.filter(date=date)