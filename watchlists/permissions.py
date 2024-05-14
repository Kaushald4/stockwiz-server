from rest_framework.permissions import BasePermission


class IsAuthorReadWriteOnly(BasePermission):
    """
        Object-level permission to only allow authors of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        
        return obj.author == request.user