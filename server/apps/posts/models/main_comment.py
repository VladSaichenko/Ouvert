from django.db import models

from apps.posts.models.posts import Post
from apps.users.models.profile import UserProfile


class MainComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
