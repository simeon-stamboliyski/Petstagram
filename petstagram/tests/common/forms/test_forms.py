from django.test import TestCase
from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Comment
from django.contrib.auth import get_user_model
from petstagram.photos.models import Photo

User = get_user_model()

class CommentFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.photo = Photo.objects.create(
            photo='https://example.com/image.jpg',
            user=self.user
        )

    def test_valid_comment_form(self):
        form_data = {'comment_text': 'Nice photo!'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form_empty_text(self):
        form_data = {'comment_text': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment_text', form.errors)

class SearchFormTests(TestCase):
    def test_valid_search_form(self):
        form_data = {'pet_name': 'Buddy'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['pet_name'], 'Buddy')

    def test_empty_search_is_valid(self):
        form_data = {'pet_name': ''}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['pet_name'], '')