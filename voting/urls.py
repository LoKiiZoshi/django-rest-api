from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Additional custom routes
app_name = 'voting'

urlpatterns = [
    # Custom endpoints
    path('poll/<int:poll_id>/vote/', views.PollViewSet.as_view({'post': 'vote'}), name='poll-vote'),
    path('poll/<int:poll_id>/results/', views.PollViewSet.as_view({'get': 'results'}), name='poll-results'),
    path('active-polls/', views.PollViewSet.as_view({'get': 'active'}), name='active-polls'),
    path('my-polls/', views.PollViewSet.as_view({'get': 'my_polls'}), name='my-polls'),
    path('my-votes/', views.VoteViewSet.as_view({'get': 'my_votes'}), name='my-votes'),
    path('completed-polls/', views.ResultViewSet.as_view({'get': 'completed'}), name='completed-polls'),
]