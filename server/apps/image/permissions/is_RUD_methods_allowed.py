from rest_framework.permissions import BasePermission

from apps.users.models.profile import UserProfile
from apps.posts.models.posts import Post
from apps.comments.models.comment import Comment


class IsUpdateAndDeleteActionsAllowed(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Permission for `POST`, `PATCH`, `DELETE` methods.
        Only owner can create images for its objects.
        """
        if isinstance(obj.content_object, UserProfile):
            return obj.content_object == request.user.profile.get()
        elif isinstance(obj.content_object, (Post, Comment)):
            return obj.content_object.profile == request.user.profile.get()
        raise Exception('Unexpected type of instance')
