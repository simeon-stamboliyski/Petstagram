from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register(request):
    return render(request, 'accounts/register-page.html')

def login(request):
    return render(request, 'accounts/login-page.html')

def details(request):
    return render(request, 'accounts/profile-details-page.html')

def delete(request):
    return render(request, 'accounts/profile-delete-page.html')

def edit(request):
    return render(request, 'accounts/profile-edit-page.html')

def logout(request, pk):
    return redirect('login')