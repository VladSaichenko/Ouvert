from rest_framework.viewsets import ModelViewSet
from url_filter.integrations.drf import DjangoFilterBackend

from apps.posts.serializers.posts import PostSerializer
from apps.posts.models.posts import Post
from apps.posts.permissions.posts import IsUserObjectOrReadOnly


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('profile',)
    permission_classes = (IsUserObjectOrReadOnly,)

    def perform_create(self, serializer):
        """ Assignment of profile """
        return serializer.save(profile=self.request.user.profile.get())
