from rest_framework.permissions import BasePermission

from django.contrib.contenttypes.models import ContentType


class IsUserProfileOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.data:
            if int(request.data['content_type']) in (9,):
                app_label = ContentType.objects.get_for_id(request.data['content_type'])
                is_exaggerated = int(request.data['object_id']) > app_label.model_class().objects.last().id
                return int(request.data['object_id']) == request.user.profile.get().id and not is_exaggerated
            return False
        return True
