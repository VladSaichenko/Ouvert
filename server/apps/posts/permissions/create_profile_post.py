from rest_framework.permissions import BasePermission


class IsUserProfileOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.data:
            if request.user and request.user.is_authenticated:
                return request.user.profile.get().__str__() == request.data['content_object']
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.profile.get().__str__() == request.data['content_object']
