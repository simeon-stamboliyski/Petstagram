from django.test import TestCase
from petstagram.pets.forms import PetForm, PetDeleteForm
from petstagram.pets.models import Pet
from django.contrib.auth import get_user_model

User = get_user_model()

class PetFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_pet_form_valid_data(self):
        form = PetForm(data={
            'name': 'Buddy',
            'date_of_birth': '2020-01-01',
            'personal_photo': 'https://example.com/image.jpg',
        })

        self.assertTrue(form.is_valid())

    def test_pet_form_missing_required_fields(self):
        form = PetForm(data={})  # no data
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('date_of_birth', form.errors)
        self.assertIn('personal_photo', form.errors)

    def test_pet_delete_form_fields_disabled_and_readonly(self):
        pet = Pet.objects.create(
            name='Max',
            date_of_birth='2019-06-01',
            personal_photo='https://example.com/pet.jpg',
            user=self.user
        )
        form = PetDeleteForm(instance=pet)

        for field_name, field in form.fields.items():
            self.assertIn('disabled', field.widget.attrs)
            self.assertIn('readonly', field.widget.attrs)