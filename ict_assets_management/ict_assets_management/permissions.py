

from rest_framework.permissions import BasePermission, SAFE_METHODS


class RoleBasedPermission(BasePermission):
    """
    Generic role-based permission.
    Each view must define:
        role_permissions = {
            "SAFE_METHODS": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
            "POST": ["ADMIN", "ASSET_MANAGER"],
            "PUT": ["ADMIN", "ASSET_MANAGER"],
            "PATCH": ["ADMIN", "ASSET_MANAGER"],
            "DELETE": ["ADMIN"],
        }
    """

    def has_permission(self, request, view):

        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        role = request.user.role.name if request.user.role else None

        # Get permission map from the view
        permission_map = getattr(view, "role_permissions", {})

        # Handle safe methods
        if request.method in SAFE_METHODS:
            allowed_roles = permission_map.get("SAFE_METHODS", [])
            return role in allowed_roles

        # Handle other methods
        allowed_roles = permission_map.get(request.method, [])
        return role in allowed_roles





