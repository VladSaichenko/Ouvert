from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.comments.serializers.comment import CommentSerializer
from apps.comments.permissions.can_user_comment import CanUserComment
from apps.comments.models.comment import Comment


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.order_by('-created')

    def get_permissions(self):
        if self.request.method == 'POST':
            return (CanUserComment(),)
        return (AllowAny(),)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile.get())
