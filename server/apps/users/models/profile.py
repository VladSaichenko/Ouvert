from django.contrib.auth.models import User
from django.db import models

from PIL import Image


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=255, blank=True)
    img = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
    location = models.CharField(max_length=125)

    following = models.ManyToManyField('self', blank=True, related_name='followed')
    likes = models.ManyToManyField('posts.Post', blank=True, related_name='likes')
    reposted = models.ManyToManyField('posts.Post', blank=True, related_name='reposted')

    def __str__(self):
        return f'{self.user.username}'

    def delete(self, *args, **kwargs):
        if self.img.name != 'default.jpg':
            self.img.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.img.path)
        if img.height > 300 or img.width > 300:
            output_size = (140, 140)
            img.thumbnail(output_size)
            img.save(self.img.path)
