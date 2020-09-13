from django.contrib.contenttypes.models import ContentType

from rest_framework.permissions import BasePermission

from apps.users.models.profile import UserProfile


class IsUserObjectOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """
        Permission for `POST` request.
        It allows creating images only for users objects.
        """
        if request.user.is_authenticated:
            if request.data:
                app_label = ContentType.objects.get_for_id(request.data['content_type'])
                instance = app_label.model_class().objects.get(id=request.data['object_id'])
                if isinstance(instance, UserProfile):
                    return instance == request.user.profile.get()
                return instance.profile == request.user.profile.get()
            return True
        return False
