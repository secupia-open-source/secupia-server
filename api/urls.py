from rest_framework_jwt.views import obtain_jwt_token

from django.urls import path

from . import views

urlpatterns = [
    # Login
    path(r'login', obtain_jwt_token, name="logout"),

    # Vehicle Endpoints
    path(r'vehicle/transactions', views.VehicleTransaction.as_view(), name="transactions"),
    
    # Flat Endpoints
    # Vehicle Endpoints
    path(r'flat/vehicles', views.FlatVehicles.as_view(), name="flat_vehicle"),
    path(r'flat/vehicles/<int:vehicle_id>', views.FlatVehicleTransactions.as_view(), 
        name="flat_transactions"),
    path(r'flat/vehicles/<int:vehicle_id>/smart-lock', views.SmartLock.as_view(), name="smart_lock"),
    # Guest Endpoint
    path(r'flat/guests', views.FlatGuest.as_view(), name="flat_guest"),
    # Notification Endpoint
    path(r'flat/registration-token', views.RegistrationToken.as_view(), name="add_reg_token"),

    # General Flat Endpoints
    # Please change the name of these endpoints
    path(r'flats/all', views.FlatView.as_view(), name="flats_all"),
    path(r'flats/with-guests', views.FlatsWithGuestsView.as_view(), name="flats_expecting_guests"),
    path(r'flats/<int:flat_id>/guests', views.GuestsInFlatView.as_view(), name="guests_in_flat"),

    # Service Endpoints
    # path(r'services/buses', views.ServiceBusView.as_view(), name="service_bus"),
    # path(r'services/staff', views.ServiceStaffView.as_view(), name="service_staff"),

    # Notice Endpoint
    # path(r'notices', views.NoticeView.as_view(), name="notices"),
    
    # Complaint Endpoint
    # path(r'complaints', views.ComplaintView.as_view(), name="complaints"),

    # Contact Endpoint
    # path(r'contacts', views.ContactView.as_view(), name="contacts"),
]