# config/urls.py
from django.contrib import admin
from django.urls import path, include
from financeiro.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),

    # Inclui as URLs nativas (login, logout, etc.)
    path('', include('django.contrib.auth.urls')), 

    # Inclui as URLs do nosso app
    path('', include('financeiro.urls')), 
]
