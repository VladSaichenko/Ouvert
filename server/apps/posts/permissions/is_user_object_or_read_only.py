from rest_framework.permissions import BasePermission


class IsUserObjectOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.profile.get() == obj.content_object
