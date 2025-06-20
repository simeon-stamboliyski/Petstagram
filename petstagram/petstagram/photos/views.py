from django.shortcuts import render, redirect
from petstagram.photos.models import Photo
from petstagram.photos.forms import PhotoCreateForm

def photo_add(request):
    form = PhotoCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'photos/photo-add-page.html', context=context)

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