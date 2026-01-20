"""
URL configuration for django_rest_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path,include

from rest_framework.routers import DefaultRouter
from voting.views import PollViewSet, VoteViewSet, ResultViewSet

# Custom Auto Router
router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'votes', VoteViewSet, basename='vote')
router.register(r'results', ResultViewSet, basename='result')



# Custom Auto Router
router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'votes', VoteViewSet, basename='vote')
router.register(r'results', ResultViewSet, basename='result')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('school.urls')),
    path('api/', include('company.urls')),
    path('api/', include('products.urls')),
     path('api/v1/', include('library_api.urls')),
    
    path('api/v1/', include('library_api.urls')),
     
     
    path('api/v1/', include(router.urls)),
    path('api/v1/voting/', include('voting.urls')),
    path('api-auth/', include('rest_framework.urls')),    
    
    
    # Authentication
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # Student app URLs
    path('', include('students.urls')),
    
    # DRF Browsable API
    path('api-auth/', include('rest_framework.urls')), 
    
    
    
   path('api/', include('banking_api.urls')),
 
]
  
