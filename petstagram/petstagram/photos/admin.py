from django.contrib import admin
from .models import Photo

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_of_publication', 'description', 'tagged_pets_list')

    @staticmethod
    def tagged_pets_list(self, obj):
        return ", ".join(p.name for p in obj.tagged_pets.all())