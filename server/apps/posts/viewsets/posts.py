from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from url_filter.integrations.drf import DjangoFilterBackend

from apps.posts.serializers.posts import PostSerializer
from apps.posts.models.posts import Post
from apps.posts.permissions.is_user_object_or_read_only import IsUserObjectOrReadOnly
from apps.posts.permissions.create_profile_post import IsUserProfileOrReadOnly


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('profile',)

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            self.permission_classes = (IsUserObjectOrReadOnly,)
        elif self.request.method == 'POST':
            self.permission_classes = (IsUserProfileOrReadOnly,)
        else:
            self.permission_classes = (AllowAny,)
        return super(PostViewSet, self).get_permissions()

    def perform_create(self, serializer):
        return serializer.save(profile=self.request.user.profile.get())
