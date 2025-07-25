from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from petstagram.pets.models import Pet

User = get_user_model()

class PetViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pet = Pet.objects.create(
            name='Buddy',
            personal_photo='https://example.com/image.jpg',
            user=self.user,
        )
        self.pet.slug = f"{self.pet.name.lower()}-{self.pet.id}"
        self.pet.save()

    def test_pet_details_view(self):
        url = reverse('pet-details', kwargs={
            'username': self.user.username,
            'pet_slug': self.pet.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pets/pet-details-page.html')
        self.assertIn('pet', response.context)

    def test_pet_add_view_get(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('pet-add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pets/pet-add-page.html')

    def test_pet_add_view_post(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('pet-add')
        response = self.client.post(url, {
            'name': 'Fluffy',
            'personal_photo': 'https://example.com/fluffy.jpg',
            'date_of_birth': '2020-01-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pet.objects.count(), 2)

    def test_pet_edit_view_get(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('pet-edit', kwargs={
            'username': self.user.username,
            'pet_slug': self.pet.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pets/pet-edit-page.html')

    def test_pet_delete_view_get_and_post(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('pet-delete', kwargs={
            'username': self.user.username,
            'pet_slug': self.pet.slug
        })

        # GET request (view confirmation page)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pets/pet-delete-page.html')

        # POST request (perform deletion)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pet.objects.filter(pk=self.pet.pk).exists())