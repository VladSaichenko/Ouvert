from rest_framework.serializers import ModelSerializer

from apps.comments.models.minor_comment import MinorComment


class MinorCommentSerializer(ModelSerializer):
    class Meta:
        model = MinorComment
        fields = ('id', 'profile', 'main_comment', 'content', 'created',)
        extra_kwargs = {'profile': {'read_only': True}}
