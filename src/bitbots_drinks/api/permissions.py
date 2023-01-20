from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsSelf(BasePermission):
    """
    A Permission which grants a requesting user access to their own user object
    """

    def has_object_permission(self, request: Request, view, obj) -> bool:
        return obj == request.user


class IsRelatedToRequester(BasePermission):
    """
    Grants users access to objects which have a link back to them using a '.user' object access
    """

    def has_object_permission(self, request: Request, view, obj) -> bool:
        return hasattr(obj, "user") and obj.user == request.user
