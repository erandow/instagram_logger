from django.db import models

class InstagramAccount(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Log(models.Model):
    instagram_account = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE)
    log_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log at {self.timestamp}: {self.log_message[:50]}..."

