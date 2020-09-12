from rest_framework.viewsets import ModelViewSet

from apps.comments.serializers.comment import CommentSerializer
from apps.comments.models.comment import Comment


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.order_by('-created')
