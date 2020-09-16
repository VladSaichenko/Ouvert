from rest_framework.serializers import RelatedField

from apps.users.models.profile import UserProfile


class ObjectPostRelatedField(RelatedField):
    """
    A custom field to use the `content_object` generic relationship in posts.
    """
    def to_representation(self, value):
        if isinstance(value, UserProfile):
            return f'{value}'
