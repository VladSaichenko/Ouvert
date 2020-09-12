from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from PIL import Image as Img

from apps.users.models.profile import UserProfile


class Image(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pictures', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(max_length=255, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Img.open(self.image.path)

        height = img.height
        width = img.width
        while height > 1080 and width > 1080:
            height -= 10
            width -= 10

        output_size = (height, width)
        img.thumbnail(output_size)
        img.save(self.image.path)
