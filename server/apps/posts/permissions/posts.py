from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUsersOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return bool(request.method in SAFE_METHODS)
