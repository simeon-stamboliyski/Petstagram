from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.pet_add.as_view(), name='add'),
    path('<str:username>/pet/<slug:pet_slug>/', views.pet_details, name='details'),
    path('<str:username>/pet/<slug:pet_slug>/edit/', views.pet_edit, name='edit'),
    path('<str:username>/pet/<slug:pet_slug>/delete/', views.pet_delete, name='delete'),
]