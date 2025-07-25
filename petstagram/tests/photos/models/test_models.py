from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from petstagram.photos.models import Photo
from petstagram.pets.models import Pet

User = get_user_model()

class PhotoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.pet1 = Pet.objects.create(name='Buddy', type='dog', user=self.user)
        self.pet2 = Pet.objects.create(name='Kitty', type='cat', user=self.user)

        self.image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg'
        )

    def test_create_photo_with_required_fields(self):
        photo = Photo.objects.create(
            photo=self.image,
            user=self.user,
        )
        self.assertEqual(photo.user.username, 'testuser')
        self.assertIsNone(photo.description)
        self.assertIsNone(photo.location)
        self.assertIsInstance(photo.photo.name, str)

    def test_create_photo_with_all_fields(self):
        photo = Photo.objects.create(
            photo=self.image,
            description='A cute moment',
            location='Sofia',
            user=self.user,
        )
        photo.tagged_pets.set([self.pet1, self.pet2])

        self.assertEqual(photo.description, 'A cute moment')
        self.assertEqual(photo.location, 'Sofia')
        self.assertEqual(photo.tagged_pets.count(), 2)
        self.assertIn(self.pet1, photo.tagged_pets.all())

    def test_photo_str_method_with_location(self):
        photo = Photo.objects.create(
            photo=self.image,
            location='Plovdiv',
            user=self.user,
        )
        self.assertEqual(str(photo), f"Photo {photo.id} - Plovdiv")

    def test_photo_str_method_without_location(self):
        photo = Photo.objects.create(
            photo=self.image,
            user=self.user,
        )
        self.assertEqual(str(photo), f"Photo {photo.id} - No location")