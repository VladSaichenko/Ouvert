from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.users.models.profile import UserProfile


class Post(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posted')
    title = models.CharField(max_length=255, null=True)
    content = models.TextField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)

    # Imply use with profile, community, etc
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Post {self.profile}'
