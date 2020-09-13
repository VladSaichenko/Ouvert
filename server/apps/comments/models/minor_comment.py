from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.users.models.profile import UserProfile
from .comment import Comment


class MinorComment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    main_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='minor_comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    images = GenericRelation('image.Image')

    def __str__(self):
        return f'{self.main_comment} Minor comment by {self.profile}'
