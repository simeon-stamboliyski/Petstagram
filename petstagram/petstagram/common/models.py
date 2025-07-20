from django.contrib.auth import get_user_model
from django.db import models
from petstagram.photos.models import Photo

UserModel = get_user_model()

class Comment(models.Model):
    comment_text = models.CharField(max_length=300)
    date_time_of_publication = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_time_of_publication']

    def __str__(self):
        return f'Comment on {self.photo_id} - {self.comment_text[:20]}...'
    
class Like(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'Like on {self.photo_id}'