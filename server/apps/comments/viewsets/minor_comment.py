from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from url_filter.integrations.drf import DjangoFilterBackend

from apps.comments.serializers.minor_comment import MinorCommentSerializer
from apps.comments.models.minor_comment import MinorComment
from apps.comments.permissions.is_user_minor_comment import IsUsersMinorCommentOrReadOnly


class MinorCommentViewSet(ModelViewSet):
    serializer_class = MinorCommentSerializer
    queryset = MinorComment.objects.order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('main_comment',)

    def get_permissions(self):
        if self.request.method == 'POST':
            return (IsAuthenticated(),)
        if self.request.method in ('DELETE', 'PUT', 'PATCH'):
            return (IsAuthenticated(), IsUsersMinorCommentOrReadOnly(),)
        return (AllowAny(),)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile.get())
