from rest_framework import permissions
from mongoengine.document import BaseDocument
from django.db.models import Model


class IsUser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to see or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # TODO: Make work with mongoengine
        # Read and write permissions are only allowed to the owner
        if isinstance(obj, Model) or isinstance(obj, BaseDocument):
            return obj.user == request.user

        return True
