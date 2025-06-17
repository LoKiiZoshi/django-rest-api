from django.contrib import admin
from .models import Poll, Choice, Vote

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'start_date', 'end_date', 'total_votes']
    list_filter = ['is_active', 'created_at', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'total_votes']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll', 'vote_count', 'vote_percentage']
    list_filter = ['poll', 'created_at']
    search_fields = ['text', 'poll__title']
    readonly_fields = ['vote_count', 'vote_percentage']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'choice', 'voted_at', 'ip_address']
    list_filter = ['voted_at', 'choice__poll']
    search_fields = ['user__username', 'choice__text']
    readonly_fields = ['voted_at']
 