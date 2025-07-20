from django.shortcuts import render, redirect
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from petstagram.photos.models import Photo
from petstagram.photos.forms import PhotoCreateForm

class photo_add(LoginRequiredMixin, views.CreateView):
    model = Photo
    form_class = PhotoCreateForm
    template_name = 'photos/photo-add-page.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.save_m2m()
        return response
    
    def get_success_url(self):
        return reverse_lazy('photos:details', kwargs={'pk': self.object.pk})

def photo_edit(request, pk):
    return render(request, 'photos/photo-edit-page.html')

def photo_details(request, pk):
    photo = Photo.objects.get(pk=pk)
    likes = photo.like_set.all()
    comments = photo.comment_set.all()

    context = {
        'photo': photo,
        'likes': likes,
        'comments': comments,
    }

    return render(request, template_name='photos/photo-details-page.html', context=context)

def photo_delete(request, pk):
    photo = Photo.objects.get(pk=pk)
    photo.delete()
    return redirect('home')