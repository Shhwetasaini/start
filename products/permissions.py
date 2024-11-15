from rest_framework import permissions

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow sellers to edit their products, and read-only access for others.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.seller == request.user
