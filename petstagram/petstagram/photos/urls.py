from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.photo_add.as_view(), name='add'),
    path('<int:pk>/', views.photo_details, name='details'),
    path('<int:pk>/edit/', views.photo_edit, name='edit'),
    path('<int:pk>/delete/', views.photo_delete, name='delete'),
]