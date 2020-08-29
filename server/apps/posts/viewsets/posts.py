from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
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
        elif self.action == 'destroy':
            permission_classes = (IsUsersOrReadOnly,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """ Assignment of profile and author """
        return serializer.save(author=self.request.user,
                               profile=self.request.user.profile.get())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)
