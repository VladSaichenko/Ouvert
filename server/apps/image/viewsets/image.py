from rest_framework.viewsets import ModelViewSet

from url_filter.integrations.drf import DjangoFilterBackend

from apps.image.serializers.image import ImageSerializer
from apps.image.models.image import Image


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('profile', 'content_type', 'object_id', 'content_object',)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile.get())
