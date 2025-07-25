from django.test import TestCase
from django.contrib.auth import get_user_model
from petstagram.accounts.models import Profile

UserModel = get_user_model()

class AppUserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = UserModel.objects.create_user(
            email='user@example.com',
            password='StrongPass123!'
        )

        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.check_password('StrongPass123!'))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)

    def test_str_returns_email(self):
        user = UserModel.objects.create_user(
            email='user@example.com',
            password='password'
        )
        self.assertEqual(str(user), 'user@example.com')

class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='test@example.com', password='testpass')

    def test_profile_created_with_default_values(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.first_name, None)
        self.assertEqual(profile.last_name, None)
        self.assertEqual(profile.date_of_birth, None)
        self.assertEqual(profile.profile_picture, None)

    def test_get_profile_name_with_first_and_last_name(self):
        profile = Profile.objects.create(
            user=self.user,
            first_name='Jane',
            last_name='Doe'
        )
        self.assertEqual(profile.get_profile_name(), 'Jane Doe')

    def test_get_profile_name_with_only_first_name(self):
        profile = Profile.objects.create(
            user=self.user,
            first_name='Jane'
        )
        self.assertEqual(profile.get_profile_name(), 'Jane')

    def test_get_profile_name_with_only_last_name(self):
        profile = Profile.objects.create(
            user=self.user,
            last_name='Doe'
        )
        self.assertEqual(profile.get_profile_name(), 'Doe')

    def test_get_profile_name_with_no_names(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.get_profile_name(), 'Anonymous User')