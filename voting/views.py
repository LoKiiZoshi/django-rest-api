from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Poll, Choice, Vote
from .serializers import (
    PollSerializer, PollCreateSerializer, VoteSerializer, 
    VoteCreateSerializer, PollResultSerializer
)

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PollCreateSerializer
        return PollSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        poll = self.get_object()
        choice_id = request.data.get('choice_id')
        
        if not choice_id:
            return Response(
                {'error': 'choice_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            choice = Choice.objects.get(id=choice_id, poll=poll)
        except Choice.DoesNotExist:
            return Response(
                {'error': 'Invalid choice for this poll'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = VoteCreateSerializer(
            data={'choice': choice.id}, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            vote = serializer.save(
                user=request.user, 
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response(
                VoteSerializer(vote).data, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        poll = self.get_object()
        serializer = PollResultSerializer(poll)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        now = timezone.now()
        active_polls = Poll.objects.filter(
            start_date__lte=now,
            end_date__gte=now,
            is_active=True
        )
        serializer = self.get_serializer(active_polls, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_polls(self, request):
        my_polls = Poll.objects.filter(created_by=request.user)
        serializer = self.get_serializer(my_polls, many=True)
        return Response(serializer.data)

class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_votes(self, request):
        votes = self.get_queryset()
        serializer = self.get_serializer(votes, many=True)
        return Response(serializer.data)

class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        now = timezone.now()
        completed_polls = Poll.objects.filter(end_date__lt=now)
        serializer = self.get_serializer(completed_polls, many=True)
        return Response(serializer.data)