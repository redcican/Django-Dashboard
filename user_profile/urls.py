from django.urls import path
from user_profile import views

urlpatterns = [
    path('profile_user/', views.user_profile_view, name='profile')
]