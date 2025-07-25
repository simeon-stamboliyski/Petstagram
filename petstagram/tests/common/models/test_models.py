from django.test import TestCase
from django.contrib.auth import get_user_model
from petstagram.photos.models import Photo
from petstagram.common.models import Comment, Like

User = get_user_model()

class CommonModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.photo = Photo.objects.create(
            photo='https://example.com/image.jpg',
            user=self.user,
        )

    def test_create_comment_successfully(self):
        comment = Comment.objects.create(
            comment_text='Beautiful photo!',
            photo=self.photo,
            user=self.user,
        )

        self.assertEqual(str(comment), f'Comment on {self.photo.id} - Beautiful photo!...')
        self.assertEqual(comment.photo, self.photo)
        self.assertEqual(comment.user, self.user)

    def test_create_like_successfully(self):
        like = Like.objects.create(
            photo=self.photo,
            user=self.user,
        )

        self.assertEqual(str(like), f'Like on {self.photo.id}')
        self.assertEqual(like.photo, self.photo)
        self.assertEqual(like.user, self.user)

    def test_comment_ordering(self):
        c1 = Comment.objects.create(comment_text="First", photo=self.photo, user=self.user)
        c2 = Comment.objects.create(comment_text="Second", photo=self.photo, user=self.user)
        comments = list(Comment.objects.all())
        self.assertEqual(comments[0], c2)
        self.assertEqual(comments[1], c1)