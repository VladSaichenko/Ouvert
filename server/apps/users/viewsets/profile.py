from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet


from apps.users.serializers.profile import UserProfileSerializer
from apps.users.models.profile import UserProfile


class UserProfileViewSet(UpdateModelMixin,
                         RetrieveModelMixin,
                         ListModelMixin,
                         GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
