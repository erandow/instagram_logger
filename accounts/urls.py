# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_account, name='create_account'),
    path('accounts/', views.account_list, name='account_list'),
    path('logs/', views.view_logs, name='view_logs'),
]

