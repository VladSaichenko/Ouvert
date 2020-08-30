from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.mixins import (
    RetrieveModelMixin, CreateModelMixin, ListModelMixin
)

from apps.posts.serializers.posts_photo import PostsPhotoSerializer
from apps.posts.models.posts_photo import PostsPhoto


class PostsPhotoViewSet(ListModelMixin,
                        CreateModelMixin,
                        RetrieveModelMixin,
                        GenericViewSet):
    serializer_class = PostsPhotoSerializer
    queryset = PostsPhoto.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """ Assignment of post """
        return serializer.save(post=serializer.validated_data['post'])
