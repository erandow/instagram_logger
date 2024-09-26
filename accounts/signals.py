# accounts/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import InstagramAccount, Log

@receiver(post_save, sender=InstagramAccount)
def create_log_on_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    Log.objects.create(account=instance, action=action, details=f"Instagram account {action.lower()}d.")

@receiver(post_delete, sender=InstagramAccount)
def create_log_on_delete(sender, instance, **kwargs):
    Log.objects.create(account=instance, action='DELETE', details="Instagram account deleted.")

