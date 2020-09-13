from rest_framework.permissions import BasePermission

from django.contrib.contenttypes.models import ContentType


class CanUserComment(BasePermission):
    def has_permission(self, request, view):
        """
        `POST` request permission for comments.
        It allows if contenttype is corresponded and does not exaggerate quantity of instances.
        """
        if request.user.is_authenticated:
            if request.data:
                app_label = ContentType.objects.get_for_id(request.data['content_type'])
                is_exaggerated = int(request.data['object_id']) > app_label.model_class().objects.last().id
                return int(request.data['content_type']) in (10, 11) and not is_exaggerated
            return True
        return False
