from rest_framework_jwt.views import obtain_jwt_token

from django.urls import path

from . import views

urlpatterns = [
    # Login/Logout
	path(r'login', obtain_jwt_token, name="logout"),
    # path(r'logout', views.Logout.as_view(), name="logout"),

    # Resident Vehile Endpoints
    # path(r'resident/vehicle', views.ResidentVehicle.as_view(), name="resident_vehicle"),

    # Guest Endpoints
    # path(r'resident/guest', views.ResidentGuest.as_view(), name="guest"),
]


# About endpoint
# Contacts endpoint
# 