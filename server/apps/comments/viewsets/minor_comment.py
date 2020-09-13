from rest_framework.viewsets import ModelViewSet

from apps.comments.serializers.minor_comment import MinorCommentSerializer
from apps.comments.models.minor_comment import MinorComment


class MinorCommentViewSet(ModelViewSet):
    serializer_class = MinorCommentSerializer
    queryset = MinorComment.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile.get())
