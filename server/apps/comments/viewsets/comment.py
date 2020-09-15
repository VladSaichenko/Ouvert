from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.comments.serializers.comment import CommentSerializer
from apps.comments.permissions.can_user_comment import CanUserComment
from apps.comments.permissions.can_user_rud_comment import CanUserRUDComment
from apps.comments.models.comment import Comment


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.order_by('-created')

    def get_permissions(self):
        if self.request.method == 'POST':
            return (IsAuthenticated(), CanUserComment(),)
        if self.request.method in ('DELETE', 'PUT', 'PATCH'):
            return (IsAuthenticated(), CanUserRUDComment(),)
        return (AllowAny(),)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile.get())
