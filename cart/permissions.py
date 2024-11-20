from rest_framework import permissions

class IsBuyerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only buyers and admins to perform actions.
    """
    def has_permission(self, request, view):
        print(f"Authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        print(f"Role: {request.user.role}")  # Check the role of the user

        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is authenticated and has a role of buyer or admin
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'buyer')
