from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.posts.models.posts import Post


@receiver(pre_delete, sender=Post)
def delete_posts_photo(sender, instance, using):
    for image in instance.images:
        image.delete()
    instance.delete()
