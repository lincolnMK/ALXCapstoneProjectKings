

from rest_framework.permissions import BasePermission, SAFE_METHODS


class RoleBasedPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(request.user.role, "name", None)

        if not hasattr(view, "role_permissions"):
            return False

        permission_map = view.role_permissions

        # Use DRF action instead of HTTP method
        action = getattr(view, "action", None)

        allowed_roles = permission_map.get(action, [])

        return role in allowed_roles




