from django.urls import path
from .views import (
    SchoolListCreateView, SchoolDetailView,
    ClassroomListCreateView, ClassroomDetailView, ClassroomBySchoolView,
    SubjectListCreateView, SubjectDetailView, SubjectBySchoolView,
    TeacherListCreateView, TeacherDetailView, TeacherBySchoolView,
    StudentListCreateView, StudentDetailView, StudentBySchoolView, StudentByClassroomView,
    ParentListCreateView, ParentDetailView, ParentByStudentView,
    ExamListCreateView, ExamDetailView, ExamByClassroomView, ExamBySubjectView,
    GradeListCreateView, GradeDetailView, GradeByStudentView, GradeByExamView,
    AttendanceListCreateView, AttendanceDetailView, AttendanceByStudentView, AttendanceByDateView
)

urlpatterns = [
    # School APIs
    path('schools/', SchoolListCreateView.as_view(), name='school-list-create'),
    path('schools/<int:pk>/', SchoolDetailView.as_view(), name='school-detail'),
     
    # Classroom APIs
    path('classrooms/', ClassroomListCreateView.as_view(), name='classroom-list-create'),
    path('classrooms/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),
    path('schools/<int:school_id>/classrooms/', ClassroomBySchoolView.as_view(), name='classroom-by-school'),
    
    # Subject APIs
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('schools/<int:school_id>/subjects/', SubjectBySchoolView.as_view(), name='subject-by-school'),
    
    # Teacher APIs
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('schools/<int:school_id>/teachers/', TeacherBySchoolView.as_view(), name='teacher-by-school'),
    
    # Student APIs
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('schools/<int:school_id>/students/', StudentBySchoolView.as_view(), name='student-by-school'),
    path('classrooms/<int:classroom_id>/students/', StudentByClassroomView.as_view(), name='student-by-classroom'),
    
    # Parent APIs
    path('parents/', ParentListCreateView.as_view(), name='parent-list-create'),
    path('parents/<int:pk>/', ParentDetailView.as_view(), name='parent-detail'),
    path('students/<int:student_id>/parents/', ParentByStudentView.as_view(), name='parent-by-student'),
    
    # Exam APIs
    path('exams/', ExamListCreateView.as_view(), name='exam-list-create'),
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('classrooms/<int:classroom_id>/exams/', ExamByClassroomView.as_view(), name='exam-by-classroom'),
    path('subjects/<int:subject_id>/exams/', ExamBySubjectView.as_view(), name='exam-by-subject'),
    
    # Grade APIs
    path('grades/', GradeListCreateView.as_view(), name='grade-list-create'),
    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade-detail'),
    path('students/<int:student_id>/grades/', GradeByStudentView.as_view(), name='grade-by-student'),
    path('exams/<int:exam_id>/grades/', GradeByExamView.as_view(), name='grade-by-exam'),
    
    # Attendance APIs
    path('attendances/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('attendances/<int:pk>/', AttendanceDetailView.as_view(), name='attendance-detail'),
    path('students/<int:student_id>/attendances/', AttendanceByStudentView.as_view(), name='attendance-by-student'),
    path('attendances/date/<str:date>/', AttendanceByDateView.as_view(), name='attendance-by-date'),
]