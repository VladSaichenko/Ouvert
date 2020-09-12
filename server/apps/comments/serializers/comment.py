from rest_framework.serializers import ModelSerializer

from apps.comments.models.comment import Comment
from .custom_fields.comment_object_related_field import CommentObjectRelatedField


class CommentSerializer(ModelSerializer):
    content_object = CommentObjectRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'profile', 'content', 'created', 'content_type', 'object_id', 'content_object',)
        extra_kwargs = {'profile': {'read_only': True},}
