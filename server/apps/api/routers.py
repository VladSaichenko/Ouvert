from rest_framework import routers

from apps.users.viewsets.views import UserViewSet
from apps.users.viewsets.profile import UserProfileViewSet
from apps.posts.viewsets.posts import PostViewSet
from apps.posts.viewsets.posts_photos import PostsPhotoViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profile', UserProfileViewSet, basename='profile')

router.register('posts', PostViewSet, basename='posts')
router.register('posts-photo', PostsPhotoViewSet, basename='posts-photo')
