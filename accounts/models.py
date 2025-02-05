from django.db import models

class InstagramAccount(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    lru = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Log(models.Model):
    instagram_account = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE)
    log_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log at {self.timestamp}: {self.log_message[:50]}..."


from django.db import models

class RetrievedAccount(models.Model):
    phone_number = models.CharField(max_length=15)  # شماره تلفن
    username = models.CharField(max_length=150)  # نام کاربری

    def __str__(self):
        return f"{self.username} - {self.phone_number}"  # نمایش نام کاربری و شماره تلفن به عنوان رشته


class ConfigSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"

    @staticmethod
    def get_setting(key, default=None):
        setting = ConfigSetting.objects.filter(key=key).first()
        return setting.value if setting else default

