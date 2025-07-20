from django.contrib.auth import get_user_model
from django.db import models
from petstagram.pets.models import Pet
from .validators import validate_file_size

UserModel = get_user_model()

class Photo(models.Model):
    photo = models.ImageField(upload_to='images', validators=[validate_file_size])
    description = models.TextField(blank=True, null=True, max_length=300)
    location = models.CharField(blank=True, null=True, max_length=30)
    tagged_pets = models.ManyToManyField(Pet, blank=True)
    date_of_publication = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo {self.id} - {self.location or 'No location'}"
    
