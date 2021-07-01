# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('request-password/', RequestPasswordResetEmailView.as_view(), name="request-password"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate"), 
    path('reset-password/<uidb64>/<token>', CompletePasswordResetView.as_view(), name="reset-password"), 
]
