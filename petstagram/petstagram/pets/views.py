from django.shortcuts import render, redirect
from django.views import generic as views
from django.urls import reverse_lazy
from petstagram.pets.models import Pet
from petstagram.pets.forms import PetForm, PetDeleteForm

def pet_details(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    all_photos = pet.photo_set.all()
    context = {
        'pet': pet,
        'all_photos': all_photos,
    }
    return render(request, template_name='pets/pet-details-page.html', context=context)

class pet_add(views.CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-add-page.html'

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        pet.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('accounts:details', kwargs={'pk': self.request.user.pk})

def pet_edit(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    if request.method == 'GET':
        form = PetForm(instance=Pet, initial=pet.__dict__)
    else:
        form = PetForm(request.POST, instance=Pet)
        if form.is_valid():
            form.save()
            return redirect('pet-details', username, pet_slug)
    context = {'form': form}
    return render(request, template_name='pets/pet-edit-page.html', context=context)

def pet_delete(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    if request.method == 'POST':
        pet.delete()
        return redirect('profile-details', pk=1)
    form = PetDeleteForm(initial=pet.__dict__)
    context = {'form': form}
    return render(request, template_name='pets/pet-delete-page.html', context=context)