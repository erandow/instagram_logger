# accounts/forms.py

from django import forms
from .models import InstagramAccount

class InstagramAccountForm(forms.ModelForm):
    class Meta:
        model = InstagramAccount
        fields = ['username', 'password']

