from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userprofile_groups',  # Unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userprofile_permissions',  # Unique related_name
    )  