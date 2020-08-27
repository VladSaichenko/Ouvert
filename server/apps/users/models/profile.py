from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField('Bio', max_length=255, blank=True)
    img = models.ImageField('Profile pic', default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.id} {self.user.username}'
