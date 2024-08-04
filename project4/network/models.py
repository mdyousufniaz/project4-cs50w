from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import localtime


class User(AbstractUser):
    followings = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }

class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000)
    creation_time = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, related_name='favourites', blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "writer": self.writer.serialize(),  # Using the User's serialize method
            "creation_time": localtime(self.creation_time).strftime('%d %B, %Y %I:%M %p'),
            "liked_users": [user.serialize() for user in self.liked_users.all()],
            "content": self.content
        }
    
    def __str__(self):
        return 'Hello'
