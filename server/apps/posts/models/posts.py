from django.db import models
from django.contrib.auth.models import User

from apps.users.models.profile import UserProfile


class Post(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posted')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(UserProfile, blank=True)
    reposts = models.ManyToManyField(UserProfile, related_name='reposted', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}'
