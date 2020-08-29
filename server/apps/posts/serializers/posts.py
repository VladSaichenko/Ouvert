from rest_framework.serializers import ModelSerializer

from apps.posts.models.posts import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'content', 'likes', 'created', 'reposts',)
