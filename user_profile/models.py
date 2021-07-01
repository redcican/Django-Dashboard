from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...")
    avatar = models.ImageField(upload_to='avatars', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    postal_code = models.IntegerField(default=0)
    about_me = models.TextField(default="about me...")

    def __str__(self):
        return f"Profile of {self.first_name} {self.last_name}"
