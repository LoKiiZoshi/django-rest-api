from django.contrib import admin
from .models import School, Classroom, Subject, Teacher, Student, Parent, Exam, Grade, Attendance

# Register School model
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'established_date')
    search_fields = ('name', 'email')
    list_filter = ('established_date',)

# Register Classroom model
@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'capacity')
    search_fields = ('name',)
    list_filter = ('school',)

# Register Subject model
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('name',)
    list_filter = ('school',)

# Register Teacher model
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'phone', 'email', 'hire_date')
    search_fields = ('user__first_name', 'user__last_name', 'email')
    list_filter = ('school', 'hire_date')

# Register Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'classroom', 'date_of_birth', 'enrollment_date')
    search_fields = ('user__first_name', 'user__last_name')
    list_filter = ('school', 'classroom', 'enrollment_date')

# Register Parent model
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student', 'phone', 'email')
    search_fields = ('user__first_name', 'user__last_name', 'email')
    list_filter = ('student',)

# Register Exam model
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'classroom', 'exam_date', 'total_marks')
    search_fields = ('subject__name',)
    list_filter = ('classroom', 'exam_date')

# Register Grade model
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'remarks')
    search_fields = ('student__user__first_name', 'student__user__last_name')
    list_filter = ('exam',)

# Register Attendance model
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    search_fields = ('student__user__first_name', 'student__user__last_name')
    list_filter = ('date', 'is_present')