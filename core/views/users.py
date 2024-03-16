from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from core.forms import UserCreationFormWithName


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationFormWithName(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('search')
    else:
        form = UserCreationFormWithName()
    return render(request, 'core/signup.html', {'form': form})
    
  
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            return redirect('search')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})