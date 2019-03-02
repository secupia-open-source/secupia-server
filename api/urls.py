from rest_framework_jwt.views import obtain_jwt_token

from django.urls import path

from . import views

urlpatterns = [
    # Login
    path(r'login', obtain_jwt_token, name="logout"),

    # Resident Profile Endpoints
    # path(r'vehicle/transactions', views.VehicleTransaction.as_view(), name="add_transaction"),
    # path(r'registration-token', views.RegistrationToken.as_view(), name="add_reg_token"),
    
    # Resident Profile Endpoints
    path(r'resident/profile', views.ResidentProfile.as_view(), name="resident_profile"),
    
    # Resident Vehile Endpoints
    path(r'resident/vehicle/<int:vehicle_id>/logs', views.ResidentVehicleTransactions.as_view(), 
        name="resident_logs"),

    # Guest Endpoints
    path(r'resident/guest', views.ResidentGuestVisit.as_view(), name="guest"),
]


# About endpoint
# Contacts endpoint
# 