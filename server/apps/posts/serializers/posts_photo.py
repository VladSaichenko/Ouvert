from rest_framework.serializers import ModelSerializer

from apps.posts.models.posts_photo import PostsPhoto


class PostsPhotoSerializer(ModelSerializer):
    class Meta:
        model = PostsPhoto
        fields = ('id', 'post', 'image',)
