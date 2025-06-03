"""
URL configuration for Petstagram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings               
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('petstagram.common.urls')),
    path('accounts/', include(('petstagram.accounts.urls', 'accounts'), namespace='accounts')),
    path('pets/', include(('petstagram.pets.urls', 'pets'), namespace='pets')),
    path('photos/', include(('petstagram.photos.urls', 'photos'), namespace='photos')),
    
]

handler404 = 'petstagram.common.views.page_404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)