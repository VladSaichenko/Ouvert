from rest_framework import routers

from apps.users.viewsets.users import UserViewSet
from apps.users.viewsets.profile import UserProfileViewSet
from apps.posts.viewsets.posts import PostViewSet
from apps.image.viewsets.image import ImageViewSet
from apps.comments.viewsets.comment import CommentViewSet
from apps.comments.viewsets.minor_comment import MinorCommentViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profile', UserProfileViewSet, basename='profile')

router.register('posts', PostViewSet, basename='posts')

router.register('images', ImageViewSet, basename='images')

router.register('comments', CommentViewSet, basename='comments')
router.register('minor-comments', MinorCommentViewSet, basename='minor-comments')
