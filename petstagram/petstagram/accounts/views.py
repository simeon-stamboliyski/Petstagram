from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, get_user_model 
from django.urls import reverse_lazy
from django.views import generic as views
from django.http import HttpResponseRedirect

from petstagram.accounts.forms import AppUserCreationForm, AppUserLoginForm
from petstagram.accounts.models import Profile

UserModel = get_user_model()

class register(views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('accounts:login')

class login(auth_views.LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'
    
    def form_valid(self, form):
        super().form_valid(form)
        profile_instance, _ = Profile.objects.get_or_create(user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())

def details(request):
    return render(request, 'accounts/profile-details-page.html')

def delete(request):
    return render(request, 'accounts/profile-delete-page.html')

def edit(request):
    return render(request, 'accounts/profile-edit-page.html')

class logout(auth_views.LogoutView):
    pass
