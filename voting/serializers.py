from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Poll, Choice, Vote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class ChoiceSerializer(serializers.ModelSerializer):
    vote_count = serializers.ReadOnlyField()
    vote_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Choice
        fields = ['id', 'text', 'description', 'vote_count', 'vote_percentage', 'created_at']

class ChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'description']

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    total_votes = serializers.ReadOnlyField()
    is_ongoing = serializers.ReadOnlyField()
    
    class Meta:
        model = Poll
        fields = [
            'id', 'title', 'description', 'created_by', 'created_at', 
            'updated_at', 'is_active', 'start_date', 'end_date', 
            'max_votes_per_user', 'choices', 'total_votes', 'is_ongoing'
        ]

class PollCreateSerializer(serializers.ModelSerializer):
    choices = ChoiceCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Poll
        fields = [
            'title', 'description', 'start_date', 'end_date', 
            'max_votes_per_user', 'choices'
        ]
    
    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data)
        
        for choice_data in choices_data:
            Choice.objects.create(poll=poll, **choice_data)
        
        return poll

class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    choice_text = serializers.CharField(source='choice.text', read_only=True)
    poll_title = serializers.CharField(source='choice.poll.title', read_only=True)
    
    class Meta:
        model = Vote
        fields = ['id', 'user', 'choice', 'choice_text', 'poll_title', 'voted_at']

class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['choice']
    
    def validate_choice(self, value):
        user = self.context['request'].user
        poll = value.poll
        
        # Check if poll is ongoing
        if not poll.is_ongoing:
            raise serializers.ValidationError("This poll is not currently active.")
        
        # Check if user has already voted maximum times
        user_votes = Vote.objects.filter(user=user, choice__poll=poll).count()
        if user_votes >= poll.max_votes_per_user:
            raise serializers.ValidationError(
                f"You have already cast the maximum number of votes ({poll.max_votes_per_user}) for this poll."
            )
        
        return value

class PollResultSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    total_votes = serializers.ReadOnlyField()
    winner = serializers.SerializerMethodField()
    
    class Meta:
        model = Poll
        fields = [
            'id', 'title', 'description', 'created_by', 'created_at',
            'end_date', 'total_votes', 'choices', 'winner'
        ]
    
    def get_winner(self, obj):
        if obj.choices.exists():
            winner_choice = max(obj.choices.all(), key=lambda c: c.vote_count)
            return {
                'choice': winner_choice.text,
                'votes': winner_choice.vote_count,
                'percentage': winner_choice.vote_percentage
            }
        return None