# instagram_log_project/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram_log_project.settings')

app = Celery('instagram_log_project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in installed apps
app.autodiscover_tasks()

# Configure the beat schedule
app.conf.beat_schedule = {
    'run-daily-at-2220-tehran': {
        'task': 'accounts.tasks.my_scheduled_task',
        'schedule': crontab(hour=22, minute=20),
        'options': {'timezone': 'Asia/Tehran'},
    },
}

# Set the default timezone for the scheduler
app.conf.timezone = 'Asia/Tehran'

