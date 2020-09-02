from django.db import models

from apps.posts.models.main_comment import MainComment
from apps.users.models.profile import UserProfile


class MinorComment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    main_comment = models.ForeignKey(MainComment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
