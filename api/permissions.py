from rest_framework import status
from rest_framework.permissions import BasePermission

from api.models import Flat

class IsFlat(BasePermission):

    def has_permission(self, request, view):
        try:
            flat = request.user.flat
            if flat is None:
                raise Flat.DoesNotExist
            return True
        except Flat.DoesNotExist:
            return False
