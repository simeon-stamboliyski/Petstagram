from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy
from petstagram.photos.models import Photo
from petstagram.common.models import Like
from petstagram.common.forms import CommentForm, SearchForm

def home(request):
    all_photos = Photo.objects.all()
    comment_form = CommentForm()
    search_form = SearchForm(request.GET)

    if search_form.is_valid():
        all_photos = all_photos.filter(
            tagged_pets__name__icontains=search_form.cleaned_data['pet_name']
        )

    context = {
        'all_photos': all_photos,
        'comment_form': comment_form,
        'search_form': search_form
    }

    return render(request, 'common/home-page.html', context=context)

def page_404(request, exception):
    return render(request, '404.html', status=404)

def like_functionality(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    liked_object = Like.objects.filter(to_photo_id=photo_id, user=request.user).first()
    
    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo=photo, user=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')

def copy_link_to_clipboard(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('photo_details', photo_id))

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')

def add_comment(request, photo_id):
    if request.method == 'POST':
        photo = Photo.objects.get(id=photo_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')