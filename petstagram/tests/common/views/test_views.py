from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from petstagram.photos.models import Photo
from petstagram.common.models import Like, Comment
from petstagram.pets.models import Pet

User = get_user_model()

class CommonViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.client.login(username='tester', password='pass123')

        self.pet = Pet.objects.create(
            name='Fluffy',
            personal_photo='https://example.com/photo.jpg',
            user=self.user,
        )

        self.photo = Photo.objects.create(
            photo='https://example.com/image.jpg',
            user=self.user,
        )
        self.photo.tagged_pets.add(self.pet)

    def test_home_view_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/home-page.html')
        self.assertIn('all_photos', response.context)

    def test_home_view_search_filtering(self):
        response = self.client.get(reverse('home'), {'pet_name': 'Fluffy'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'https://example.com/image.jpg')

    def test_like_photo_and_unlike(self):
        response_like = self.client.post(reverse('like', kwargs={'photo_id': self.photo.id}), follow=True)
        self.assertEqual(Like.objects.count(), 1)

        response_unlike = self.client.post(reverse('like', kwargs={'photo_id': self.photo.id}), follow=True)
        self.assertEqual(Like.objects.count(), 0)

    def test_add_comment_to_photo(self):
        response = self.client.post(reverse('comment', kwargs={'photo_id': self.photo.id}), {
            'comment_text': 'Nice photo!'
        }, follow=True)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().comment_text, 'Nice photo!')

    def test_404_page_rendering(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')