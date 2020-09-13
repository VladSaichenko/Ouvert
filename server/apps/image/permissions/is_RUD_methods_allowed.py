from rest_framework.permissions import BasePermission

from apps.users.models.profile import UserProfile
from apps.posts.models.posts import Post
from apps.comments.models.comment import Comment


class IsUpdateAndDeleteActionsAllowed(BasePermission):
    # def has_permission(self, request, view):
    #     """
    #     Permission for `POST`, `PATCH`, `DELETE` methods.
    #     """
    #     if request.user.is_authenticated:
    #         print(request.data)
    #         app_label = ContentType.objects.get_for_id(request.data['content_type'])
    #         instance = app_label.model_class().objects.get(id=request.data['object_id'])
    #         if isinstance(instance, UserProfile):
    #             return instance == request.user.get()
    #         elif isinstance(instance, (Post, Comment)):
    #             return instance.profile == request.user.get()
    #         raise Exception('Unexpected type of instance')

    def has_object_permission(self, request, view, obj):
        """
        Permission for `POST`, `PATCH`, `DELETE` methods.
        Only owner can create images for its objects.
        """
        if request.user.is_authenticated:
            if isinstance(obj.content_object, UserProfile):
                return obj.content_object == request.user.profile.get()
            elif isinstance(obj.content_object, (Post, Comment)):
                return obj.content_object.profile == request.user.profile.get()
            raise Exception('Unexpected type of instance')
        return False
