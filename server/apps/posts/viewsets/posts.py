from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
)

from url_filter.integrations.drf import DjangoFilterBackend

from apps.posts.serializers.posts import PostSerializer
from apps.posts.models.posts import Post
from apps.posts.permissions.posts import IsUsersOrReadOnly


class PostViewSet(RetrieveModelMixin,
                  CreateModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('profile', 'author',)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (IsAuthenticated,)
        elif self.action == ('destroy' or 'update'):
            permission_classes = (IsUsersOrReadOnly,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """ Assignment of profile and author """
        return serializer.save(author=self.request.user,
                               profile=self.request.user.profile.get())
