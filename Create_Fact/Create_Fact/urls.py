from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from fact.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fact/', include('fact.urls')),
    path('', home, name='home'),
]