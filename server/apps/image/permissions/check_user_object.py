from django.contrib.contenttypes.models import ContentType

from rest_framework.permissions import BasePermission

from apps.users.models.profile import UserProfile


class IsUserObjectOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """
        Permission for `POST` request.
        It allows creating images only for users objects.
        Contenttype can be only UserProfile, Post, Comment, MinorComment.
        """
        if request.data and int(request.data['content_type']) in (9, 10, 12, 13):
            app_label = ContentType.objects.get_for_id(request.data['content_type'])
            instance = app_label.model_class().objects.get(id=request.data['object_id'])
            if isinstance(instance, UserProfile):
                return instance == request.user.profile.get()
            return instance.profile == request.user.profile.get()
        return True
