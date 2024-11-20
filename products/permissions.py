from rest_framework import permissions

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only sellers and admins to create/modify products.
    Buyers and unauthenticated users will have read-only access.
    """
    def has_permission(self, request, view):
        print(f"Authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        print(f"Is staff (admin): {request.user.is_staff}")
        print(f"Is seller: {request.user.is_seller}")  # Using is_seller from CustomUser
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is authenticated and either admin or seller
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_seller)

    def has_object_permission(self, request, view, obj):
        print(f"Object permission check for: {obj}")
        if request.method in permissions.SAFE_METHODS:
            return True

        # Ensure the user is either the seller or an admin
        return obj.seller == request.user or request.user.is_staff
