from rest_framework.serializers import RelatedField

from apps.posts.models.posts import Post
from apps.image.models.image import Image


class CommentObjectRelatedField(RelatedField):
    """
    A custom field to use the `content_object` generic relationship with comments.
    """
    def to_representation(self, value):
        if isinstance(value, Image):
            return f'{value}'
        if isinstance(value, Post):
            return f'{value}'
        raise Exception('Unexpected type of tagged object')
