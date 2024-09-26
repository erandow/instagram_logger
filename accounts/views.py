# Create your views here.

# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import InstagramAccount, Log
from .forms import InstagramAccountForm

@login_required
def create_account(request):
    if request.method == 'POST':
        form = InstagramAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_list')
    else:
        form = InstagramAccountForm()
    return render(request, 'accounts/create_account.html', {'form': form})

@login_required
def account_list(request):
    accounts = InstagramAccount.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

@login_required
def view_logs(request):
    logs = Log.objects.all()
    return render(request, 'accounts/logs.html', {'logs': logs})

