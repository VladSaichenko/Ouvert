from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

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

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return (IsUserObjectOrReadOnly(),)
        elif self.request.method == 'POST':
            return (IsAuthenticated(),)
        else:
            return (AllowAny(),)

    def perform_create(self, serializer):
        """ Assignment of profile """
        print('!!!!!!!!!!!!!!!!', serializer.validated_data['content_object']['content_object'])
        post_instance = Post(
            profile=self.request.user.profile.get(),
            content_object=serializer.validated_data['content_object']['content_object'],
            title=serializer.validated_data['title'],
            content=serializer.validated_data['content'],
        )
        post_instance.save()

        return self.get_serializer(instance=post_instance)
