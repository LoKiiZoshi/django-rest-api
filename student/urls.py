
# 4. URLS.PY - Student App URLs
# students/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)

app_name = 'students'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Custom API endpoints
    path('api/students/<uuid:pk>/enroll/', 
         views.StudentViewSet.as_view({'post': 'enroll'}), 
         name='student-enroll'),
    
    path('api/students/statistics/', 
         views.StudentViewSet.as_view({'get': 'statistics'}), 
         name='student-statistics'),
    
    path('api/courses/popular/', 
         views.CourseViewSet.as_view({'get': 'popular'}), 
         name='popular-courses'),
    
    path('api/enrollments/by-student/', 
         views.EnrollmentViewSet.as_view({'get': 'by_student'}), 
         name='enrollments-by-student'),
]