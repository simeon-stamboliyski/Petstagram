from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from petstagram.accounts.models import Profile
from petstagram.photos.models import Photo

UserModel = get_user_model()

class AccountsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='test@example.com', password='testpass')
        self.profile = Profile.objects.create(user=self.user)

    def test_register_view_GET(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register-page.html')

    def test_register_view_POST_creates_user(self):
        response = self.client.post(reverse('accounts:register'), {
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertEqual(UserModel.objects.filter(email='newuser@example.com').count(), 1)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_login_view_GET(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login-page.html')

    def test_login_view_POST_authenticates_user(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': self.user.email,
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_profile_details_view_context(self):
        self.client.login(email=self.user.email, password='testpass')
        response = self.client.get(reverse('accounts:details', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile_user'], self.user)
        self.assertIn('user_photos', response.context)
        self.assertIn('user_pets', response.context)
        self.assertIn('total_likes_count', response.context)

    def test_profile_edit_view_GET(self):
        self.client.login(email=self.user.email, password='testpass')
        response = self.client.get(reverse('accounts:edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile-edit-page.html')

    def test_profile_edit_view_POST_updates_profile(self):
        self.client.login(email=self.user.email, password='testpass')
        response = self.client.post(reverse('accounts:edit'), {
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '2000-01-01',
            'profile_picture': 'https://example.com/img.png'
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Test')
        self.assertRedirects(response, reverse('accounts:details', kwargs={'pk': self.user.pk}))

    def test_profile_delete_view_deletes_user(self):
        self.client.login(email=self.user.email, password='testpass')
        response = self.client.post(reverse('accounts:delete'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(UserModel.objects.filter(pk=self.user.pk).exists())

    def test_logout_view_redirects(self):
        self.client.login(email=self.user.email, password='testpass')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)