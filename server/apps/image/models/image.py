from django.db import models

from PIL import Image

from apps.posts.models.posts import Post


class PostsPhoto(models.Model):
    # profile
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='post_pictures', blank=True)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        height = img.height
        width = img.width
        while height > 1280 and width > 720:
            height -= 100
            width -= 100

        output_size = (height, width)
        img.thumbnail(output_size)
        img.save(self.image.path)
