from django.contrib.auth.models import User
from django.db import models

from PIL import Image


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField('Bio', max_length=255, blank=True)
    img = models.ImageField('Profile pic', default='default.jpg', upload_to='profile_pics', blank=True)

    following = models.ManyToManyField(User, related_name='followed', blank=True)

    def __str__(self):
        return f'{self.user.username}'

    def delete(self, *args, **kwargs):
        if self.img:
            self.img.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.img.path)
        if img.height > 300 or img.width > 300:
            output_size = (140, 140)
            img.thumbnail(output_size)
            img.save(self.img.path)
