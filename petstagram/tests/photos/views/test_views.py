from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from petstagram.photos.models import Photo
from petstagram.pets.models import Pet

User = get_user_model()

class PhotoViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.pet = Pet.objects.create(name='Buddy', type='dog', user=self.user)

        self.image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg'
        )

        self.photo = Photo.objects.create(
            photo=self.image,
            description='Test description',
            user=self.user
        )
        self.photo.tagged_pets.add(self.pet)

    def test_photo_add_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('photos:add'))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('photos:add')}")

    def test_photo_add_view_creates_photo_if_logged_in(self):
        self.client.login(username='testuser', password='pass123')
        image = SimpleUploadedFile('img.jpg', b'123', content_type='image/jpeg')

        response = self.client.post(reverse('photos:add'), {
            'photo': image,
            'description': 'A test photo',
            'location': 'Test city',
            'tagged_pets': [self.pet.pk],
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Photo.objects.filter(description='A test photo').exists())

    def test_photo_details_view_returns_200(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('photos:details', kwargs={'pk': self.photo.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test description')

    def test_photo_delete_view_removes_photo(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(reverse('photos:delete', kwargs={'pk': self.photo.pk}), follow=True)

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Photo.objects.filter(pk=self.photo.pk).exists())