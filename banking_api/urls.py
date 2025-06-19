from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AccountViewSet, TransactionViewSet, LoanViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = [
    path('', include(router.urls)),
]