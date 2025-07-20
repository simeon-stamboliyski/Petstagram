from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, get_user_model 
from django.urls import reverse_lazy
from django.views import generic as views
from django.http import HttpResponseRedirect

from petstagram.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm
from petstagram.accounts.models import Profile
from petstagram.photos.models import Photo

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

class details(views.DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['user_photos'] = (
            Photo.objects
                .filter(user_id=self.object.pk)
                .order_by('-date_of_publication')
        )
        context['user_pets'] = user.pet_set.all()
        context['total_likes_count'] = sum(p.like_set.count() for p in user.photo_set.all())
        return context

class delete(views.DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return redirect(self.get_success_url())

class edit(views.UpdateView):
    model = UserModel
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_object(self, queryset=None):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse_lazy(
            'details',
            kwargs={'pk': self.object.pk}
        )

class logout(auth_views.LogoutView):
    pass
