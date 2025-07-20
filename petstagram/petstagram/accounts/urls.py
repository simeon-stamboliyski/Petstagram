from django.urls import path
from petstagram.accounts import views

urlpatterns = [
    path('register/', views.register.as_view(), name='register'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout.as_view(), name='logout'),
    path('profile/<int:pk>/', views.details, name='details'),
    path('profile/<int:pk>/edit/', views.edit.as_view(), name='edit'),
    path('profile/<int:pk>/delete/', views.delete, name='delete'),
]