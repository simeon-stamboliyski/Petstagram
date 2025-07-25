from django.test import TestCase
from django.contrib.auth import get_user_model
from petstagram.pets.models import Pet

User = get_user_model()

class PetModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_create_pet_with_valid_data(self):
        pet = Pet.objects.create(
            name='Buddy',
            personal_photo='https://example.com/buddy.jpg',
            date_of_birth='2020-01-01',
            user=self.user
        )
        self.assertEqual(pet.name, 'Buddy')
        self.assertEqual(pet.user, self.user)
        self.assertEqual(pet.personal_photo, 'https://example.com/buddy.jpg')
        self.assertEqual(str(pet), 'Buddy')

    def test_slug_is_generated_after_save(self):
        pet = Pet(
            name='Buddy',
            personal_photo='https://example.com/buddy.jpg',
            date_of_birth='2020-01-01',
            user=self.user
        )
        self.assertIsNone(pet.slug)  # Slug should not exist before saving
        pet.save()
        self.assertTrue(pet.slug.startswith('buddy-'))
        self.assertIn(str(pet.id), pet.slug)

    def test_str_method_returns_name(self):
        pet = Pet.objects.create(
            name='Fluffy',
            personal_photo='https://example.com/fluffy.jpg',
            user=self.user
        )
        self.assertEqual(str(pet), 'Fluffy')