from rest_framework.serializers import ModelSerializer

from apps.posts.models.posts import Post
from apps.users.models.profile import UserProfile
from .custom_fields.object_post_related_field import ObjectPostRelatedField


class PostSerializer(ModelSerializer):
    content_object = ObjectPostRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'profile', 'created', 'title', 'content', 'content_type', 'object_id', 'content_object',
        )
        extra_kwargs = {
            'profile': {'read_only': True},
            'content_object': {'read_only': True},
        }
