from rest_framework.serializers import ModelSerializer

from apps.image.models.image import Image
from .custom_fields.image_object_related_field import ImageObjectRelatedField


class ImageSerializer(ModelSerializer):
    content_object = ImageObjectRelatedField(read_only=True)

    class Meta:
        model = Image
        fields = (
            'id', 'profile', 'caption', 'created', 'image', 'content_type', 'object_id', 'content_object',
        )
        extra_kwargs = {'profile': {'read_only': True}}
