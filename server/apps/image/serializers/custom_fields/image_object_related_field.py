from rest_framework.serializers import RelatedField

from apps.users.models.profile import UserProfile
from apps.posts.models.posts import Post
from apps.comments.models.comment import Comment
from apps.comments.models.minor_comment import MinorComment


class ImageObjectRelatedField(RelatedField):
    """
    A custom field to use the `content_object` generic relationship with images.
    """
    def to_representation(self, value):
        if isinstance(value, (UserProfile, Post, Comment, MinorComment,)):
            return f'{value}'
        raise Exception('Unexpected type of tagged object')
