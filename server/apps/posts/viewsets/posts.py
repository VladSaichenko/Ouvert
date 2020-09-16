from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from url_filter.integrations.drf import DjangoFilterBackend

from apps.posts.serializers.posts import PostSerializer
from apps.posts.models.posts import Post
from apps.posts.permissions.is_user_object_or_read_only import IsUserObjectOrReadOnly
from apps.posts.permissions.create_profile_post import IsUserProfileOrReadOnly


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('profile', 'created', 'content_type', 'object_id', 'content_object',)

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return (IsUserObjectOrReadOnly(),)
        elif self.request.method == 'POST':
            return (IsAuthenticated(), IsUserProfileOrReadOnly(),)
        return (AllowAny(),)

    def perform_create(self, serializer):
        return serializer.save(profile=self.request.user.profile.get())
