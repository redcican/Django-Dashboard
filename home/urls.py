from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
