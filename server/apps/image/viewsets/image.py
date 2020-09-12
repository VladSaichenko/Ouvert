from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from url_filter.integrations.drf import DjangoFilterBackend

from apps.image.permissions.check_user_object import IsUserObjectOrReadOnly
from apps.image.serializers.image import ImageSerializer
from apps.image.models.image import Image


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('profile', 'content_type', 'object_id', 'content_object',)
    # permission_classes = (IsUserObjectOrReadOnly,)

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = (IsUserObjectOrReadOnly,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile.get())
