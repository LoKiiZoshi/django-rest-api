from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, register, logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Add this line

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)  

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]