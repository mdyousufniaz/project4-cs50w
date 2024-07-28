from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followings = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')

class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000)
    creation_time = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, related_name='favourites', blank=True)
