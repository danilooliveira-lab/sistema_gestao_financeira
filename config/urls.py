# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inclui as URLs nativas (login, logout, etc.)
    path('', include('django.contrib.auth.urls')), 

    # Inclui as URLs do nosso app
    path('', include('financeiro.urls')), 
]