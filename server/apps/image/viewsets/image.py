from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from url_filter.integrations.drf import DjangoFilterBackend

from apps.image.permissions.check_user_object import IsUserObjectOrReadOnly
from apps.image.permissions.is_RUD_methods_allowed import IsUpdateAndDeleteActionsAllowed

from apps.image.serializers.image import ImageSerializer
from apps.image.models.image import Image


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('profile', 'content_type', 'object_id', 'content_object',)

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return (IsUpdateAndDeleteActionsAllowed(),)
        if self.request.method == 'POST':
            return (IsUserObjectOrReadOnly(),)
        else:
            return (AllowAny(),)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile.get())
