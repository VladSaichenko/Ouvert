from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.users.serializers.profile import UserProfileSerializer
from apps.users.models.profile import UserProfile
from apps.users.permissions.profile import IsUsersProfileOrReadOnly


class UserProfileViewSet(RetrieveModelMixin,
                         UpdateModelMixin,
                         GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsUsersProfileOrReadOnly, )
