from rest_framework.serializers import RelatedField

from apps.users.models.profile import UserProfile
from apps.posts.models.posts import Post


class ImageObjectRelatedField(RelatedField):
    """
    A custom field to use the `content_object` generic relationship with images.
    """
    def to_representation(self, value):
        if isinstance(value, UserProfile):
            return f'{value}'
        if isinstance(value, Post):
            return f'{value}'
        raise Exception('Unexpected type of tagged object')
