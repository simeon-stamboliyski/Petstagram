from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('like/<int:photo_id>/', views.like_functionality, name="like"),
    path('share/<int:photo_id>/', views.copy_link_to_clipboard, name="share"),
    path('comment/<int:photo_id>/', views.add_comment, name="comment"),
]