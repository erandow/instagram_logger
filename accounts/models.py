# Create your models here.

# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class InstagramAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # You can encrypt this for production
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class Log(models.Model):
    ACTION_TYPES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    )

    account = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=6, choices=ACTION_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField()

    def __str__(self):
        return f"{self.account.username} - {self.action} at {self.timestamp}"

