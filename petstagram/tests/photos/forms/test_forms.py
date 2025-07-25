from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from petstagram.photos.forms import PhotoCreateForm, PhotoEditForm
from petstagram.pets.models import Pet  # adjust if different
from petstagram.photos.models import Photo

User = get_user_model()

class PhotoFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.pet = Pet.objects.create(name='Buddy', type='dog', user=self.user)

        self.image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg'
        )

    def test_photo_create_form_valid(self):
        form_data = {
            'description': 'A nice photo',
            'location': 'Sofia',
            'pets': [self.pet.id],
        }
        form_files = {'photo': self.image}

        form = PhotoCreateForm(data=form_data, files=form_files)

        self.assertTrue(form.is_valid())
        self.assertNotIn('user', form.fields)

    def test_photo_create_form_missing_required(self):
        form = PhotoCreateForm(data={}, files={})

        self.assertFalse(form.is_valid())
        self.assertIn('photo', form.errors)

    def test_photo_edit_form_valid(self):
        photo = Photo.objects.create(
            photo=self.image,
            description='Test photo',
            location='Plovdiv',
            user=self.user,
        )
        photo.pets.add(self.pet)

        form_data = {
            'description': 'Updated description',
            'location': 'Burgas',
            'pets': [self.pet.id],
        }

        form = PhotoEditForm(data=form_data, instance=photo)

        self.assertTrue(form.is_valid())
        self.assertNotIn('photo', form.fields)

    def test_photo_edit_form_missing_description(self):
        photo = Photo.objects.create(
            photo=self.image,
            description='Original',
            location='Varna',
            user=self.user,
        )
        photo.pets.add(self.pet)

        form_data = {
            'location': 'New place',
            'pets': [self.pet.id],
        }

        form = PhotoEditForm(data=form_data, instance=photo)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)