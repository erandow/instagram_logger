from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import RetrievedAccount
from .models import InstagramAccount
from .models import Log

admin.site.register(RetrievedAccount)
admin.site.register(InstagramAccount)
admin.site.register(Log)


