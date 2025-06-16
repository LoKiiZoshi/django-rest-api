from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, EmployeeViewSet, ProjectViewSet, TaskViewSet, ClientViewSet,MediaUploadViewSet,CompanyViewSet,CompanyBlogViewSet


router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'clients', ClientViewSet) 
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'company-blogs', CompanyBlogViewSet, basename='companyblog')
router.register(r'media-upload', MediaUploadViewSet)

 
 


urlpatterns = [
    path('', include(router.urls)), 
 
]




 
  