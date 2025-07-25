from django.test import TestCase
from django.contrib.auth import get_user_model
from petstagram.accounts.forms import (
    AppUserCreationForm,
    AppUserLoginForm,
    AppUserChangeForm,
    ProfileEditForm,
)
from petstagram.accounts.models import Profile

UserModel = get_user_model()

class AppUserCreationFormTests(TestCase):
    def test_valid_data_creates_user(self):
        form = AppUserCreationForm(data={
            'email': 'user@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'user@example.com')

    def test_passwords_do_not_match(self):
        form = AppUserCreationForm(data={
            'email': 'user@example.com',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass456!',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class AppUserLoginFormTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@example.com', password='StrongPass123!')

    def test_login_valid_data(self):
        form = AppUserLoginForm(data={
            'username': 'user@example.com',
            'password': 'StrongPass123!',
        })
        self.assertTrue(form.is_valid())

    def test_login_invalid_data(self):
        form = AppUserLoginForm(data={
            'username': 'user@example.com',
            'password': 'WrongPassword!',
        })
        self.assertFalse(form.is_valid())

class AppUserChangeFormTests(TestCase):
    def test_change_email(self):
        user = UserModel.objects.create_user(email='old@example.com', password='testpass')
        form = AppUserChangeForm(instance=user, data={
            'email': 'new@example.com'
        })

        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, 'new@example.com')

class ProfileEditFormTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@example.com', password='testpass')
        self.profile = Profile.objects.create(user=self.user)

    def test_edit_profile_valid_data(self):
        form = ProfileEditForm(instance=self.profile, data={
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-01',
            'profile_picture': 'https://example.com/image.jpg'
        })

        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.first_name, 'John')
        self.assertEqual(updated_profile.last_name, 'Doe')