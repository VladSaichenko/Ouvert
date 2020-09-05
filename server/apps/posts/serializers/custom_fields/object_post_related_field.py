from rest_framework.serializers import RelatedField
from rest_framework.serializers import ValidationError

from django.contrib.auth.models import User
from apps.users.models.profile import UserProfile


class ObjectPostRelatedField(RelatedField):
    """
    A custom field to use the `content_object` generic relationship in posts.
    """
    def to_representation(self, value):
        if isinstance(value, UserProfile):
            return f'{value}'

    def to_internal_value(self, data):
        user = User.objects.get(username=data.split()[1])

        if not data:
            raise ValidationError('This field is required.')

        return UserProfile.objects.get(id=user.id)
