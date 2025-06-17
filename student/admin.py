from django.contrib import admin
from .models import Student, Course, Enrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'email', 'status', 'enrollment_date']
    list_filter = ['status', 'gender', 'enrollment_date']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('student_id', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'address', 'profile_image')
        }),
        ('Academic Information', {
            'fields': ('status', 'enrollment_date')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'instructor', 'credits', 'difficulty', 'is_active']
    list_filter = ['difficulty', 'is_active', 'credits']
    search_fields = ['code', 'name', 'instructor']
    readonly_fields = ['id', 'created_at']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'grade', 'enrollment_date']
    list_filter = ['status', 'grade', 'enrollment_date']
    search_fields = ['student__student_id', 'course__code', 'course__name']
    readonly_fields = ['id', 'enrollment_date']