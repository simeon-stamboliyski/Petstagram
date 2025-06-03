from django.contrib import admin
from .models import Comment, Like

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('photo', 'comment_text', 'date_time_of_publication')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('photo',)