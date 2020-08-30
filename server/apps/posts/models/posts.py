from django.db import models

from apps.users.models.profile import UserProfile


class Post(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posted')
    content = models.TextField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}'
