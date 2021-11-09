from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from rest_framework.request import Request

from .authentication import ServiceAccountAuthentication


class IsServiceAccount(BasePermission):
    """
    A Permission which grants access to requests if they are authenticated using the service account token.
    """

    def has_permission(self, request: Request, view) -> bool:
        return request.auth == ServiceAccountAuthentication

    def has_object_permission(self, request: Request, view, obj) -> bool:
        return request.auth == ServiceAccountAuthentication


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
