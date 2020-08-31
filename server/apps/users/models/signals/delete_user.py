from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from apps.users.models.profile import UserProfile


@receiver(post_delete, sender=UserProfile)
def create_user_profile(sender, instance, using, **kwargs):
    user = User.objects.get(username=instance.user.username)
    user.delete()
