from django.contrib.contenttypes.models import ContentType

from rest_framework.permissions import BasePermission

from apps.users.models.profile import UserProfile
from apps.posts.models.posts import Post
from apps.comments.models.comment import Comment


class IsUserObjectOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.data:
            print('data >>>', request.data)
            app_label = ContentType.objects.get_for_id(request.data['content_type'])
            instance = app_label.model_class().objects.get(id=request.data['object_id'])
            if isinstance(instance, UserProfile):
                return instance == request.user.profile.get()
            return instance.profile == request.user.profile.get()
        return True