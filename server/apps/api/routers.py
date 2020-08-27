from rest_framework import routers

from apps.users.viewsets.views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
