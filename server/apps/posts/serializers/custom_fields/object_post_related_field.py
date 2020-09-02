from rest_framework.serializers import RelatedField
from rest_framework.serializers import ValidationError

from django.contrib.auth.models import User
from apps.users.models.profile import UserProfile


class ObjectPostRelatedField(RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """

    def to_representation(self, value):
        if not isinstance(value, UserProfile):
            print(type(value), value)

        if isinstance(value, UserProfile):
            return f'{value}'
        raise Exception('Unexpected type of content object')

    def to_internal_value(self, data):
        user = User.objects.get(username=data.split()[1])

        if not data:
            raise ValidationError({
                'content_object': 'This field is required.'
            })
        return {
            'content_object': UserProfile.objects.get(id=user.id)
        }
