from django.urls import path, include
from petstagram.accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/<int:pk>/', views.details, name='details'),
    path('profile/<int:pk>/edit/', views.edit, name='edit'),
    path('profile/<int:pk>/delete/', views.delete, name='delete'),
]