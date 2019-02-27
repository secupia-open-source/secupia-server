from rest_framework import status
from rest_framework.permissions import BasePermission

from api.models import UserProfile

class IsResident(BasePermission):

	def has_permission(self, request, view):
		profile = request.user.profile
		if profile.is_resident:
			return True
		else:
			return False