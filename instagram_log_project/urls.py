from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page URL
    path('create_account/', views.create_instagram_account, name='create_instagram_account'),
    path('log_message/', views.log_message, name='log_message'),
    path('accounts/', views.account_list, name='account_list'),
    path('logs/', views.log_list, name='log_list'),
    path('start_task/', views.start_task, name='start_task'),  # URL to start the Celery task

]

