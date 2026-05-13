from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings  # Add this
from django.conf.urls.static import static  # Add this
from services.models import Category, Service
from accounts.models import UserProfile
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),  # Added this
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)