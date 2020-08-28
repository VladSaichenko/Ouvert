from rest_framework import routers

from apps.users.viewsets.views import UserViewSet
from apps.users.viewsets.profile import UserProfileViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profile', UserProfileViewSet, basename='profile')
