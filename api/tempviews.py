from firebase_admin import firestore, messaging

from django.contrib.auth import logout

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.models import GuestVisit, Vehicle
from api.permissions import IsResident
from api.utils import validate_vehicle_log_data, validate_guest_visit_data


class RegistrationToken(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        print(data)
        registration_token = data['registration_token']
        profile = request.user.profile
        profile.registration_token = registration_token
        profile.save()

        response_data = {'message': "Request Successful"}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)

class ResidentProfile(APIView):

    permission_classes = (IsAuthenticated, IsResident)

    def get(self, request):
        '''Return profile information of Resident'''
        resident = request.user.profile.resident
        vehicles = resident.vehicles.all()

        resident_serializer = serializers.ResidentSerializer(resident)
        vehicle_serializer = serializers.ResidentVehicleSerializer(vehicles, many=True)

        response_data = {
            "profile": resident_serializer.data,
            "vehicle": vehicle_serializer.data
        }
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class ResidentVehicle(APIView):

    permission_classes = (IsAuthenticated, IsResident)

    def get(self, request):
        '''Return profile information of Resident'''
        resident = request.user.profile.resident
        
        vehicles = resident.vehicles.all()
        serializer = serializers.ResidentVehicleSerializer(vehicles, many=True)

        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class ResidentVehicleLog(APIView):

    permission_classes = (IsAuthenticated, IsResident)

    def get(self, request, vehicle_id):
        '''Return profile information of Resident'''
        resident = request.user.profile.resident
        
        vehicle = resident.vehicles.get(id=vehicle_id)
        serializer = serializers.ResidentVehicleLogSerializer(vehicle.vehicle.transactions, many=True)

        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class VehicleTransaction(APIView):

    permission_classes = (IsAuthenticated,)

    def sendNotification(self, registration_token, transaction):
        title = 'Order {}'.format(order_status)

        if is_entry:
            body = "Your vehicle {} has entered"
        else:
            body = "Your vehicle {} has exited"
        body.format(transaction.vehicle.license_plate)

        message = messaging.Message(
            notification = messaging.Notification(
                title = title,
                body = body,
            ),
            token = registration_token,
        )

        try:
            response = messaging.send(message)
            print(response)
        except Exception as e:
            print(e)

    def post(self, request):
        '''Add vehicle transaction and send notification to resident'''
        data = request.data
        print(data)
        try:
            license_plate, is_entry, reg_token = validate_vehicle_log_data(data)
        except ValueError:
            response_data = {'message': 'Invalid request'}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)
        except Exception as e:
            print(e)
        vehicle, _ = Vehicle.objects.get_or_create(license_plate=license_plate)
        transaction = vehicle.add_transaction(is_entry)

        # vehicle.send_notification(reg_token, transaction)

        response_data = {'message': 'Transaction added'}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class ResidentGuestVisit(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''Return all Guest visits for a Resident'''
        resident = request.user.profile.resident

        guest_visits = resident.get_active_guest_visits()
        serializer = serializers.GuestVisitSerializer(guest_visits, many=True)

        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


    def post(self, request):
        '''Add a new Guest visit to a Resident'''
        '''Development Notes:
        add expected_date_time field
        '''
        flat = request.user.profile.resident.flat

        data = request.data
        try:
            guest_data, visit_data = validate_guest_visit_data(data)
        except ValueError:
            response_data = {'message': "Invalid request"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)

        guest_visit_id = flat.add_guest_visit(guest_data, visit_data)

        response_data = {
            'message': "Guest added",
            'id': guest_visit_id
        }
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)

    def patch(self, request):
        '''Update an existing Guest visit to a Resident'''
        data = request.data
        try:
            guest_visit = GuestVisit.objects.get(id=data['guest_id'])
            guest_data, visit_data = validate_guest_visit_data(data)
        except GuestVisit.DoesNotExist:
            response_data = {'message': "Guest does not exist"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response_data, status_code)
        except ValueError:
            response_data = {'message': "Invalid format or fields may be missing"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)

        guest_profile = guest_visit.guest.profile
        guest_profile.name = guest_data['name']
        guest_profile.contact = guest_data['contact']
        guest_profile.save()

        guest_visit.purpose = visit_data['purpose']
        guest_visit.save()

        response_data = {'message': "Guest updated"}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


    def delete(self, request):
        '''Delete a Guest visit to a Resident'''
        data = request.data
        try:
            guest_visit = GuestVisit.objects.get(id=data['guest_id'])
        except GuestVisit.DoesNotExist:
            response_data = {'message': "Guest does not exist"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response_data, status_code)
        guest_visit.delete()

        response_data = {'message': "Guest updated"}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)

# class ResidentServiceVisit(APIView):

#     def get(self, request):
#         '''Return all Service visits Resident has subcribed to'''
#         resident = Resident.objects.get(user=request.user)
#         subscribed_services = resident.get_subscribed_services()
#         serializer = ServiceVisitSerializer(subscribed_services, many=True)

#         response_data = serializer.data
#         status_code = status.HTTP_200_OK

#         return Response(response_data, status_code)


#     def post(self, request):
#         '''Add a new Service visit to Resident\'s subscirptions'''
#         pass


#     def delete(self, request):
#         '''Delete a Service visit from a Resident\'s subscirptions'''
#         pass


# class AdminServiceVisit(APIView):

#     def get(self, request):
#         '''Return all Service visits'''
#         services = Service.objects.active_services()
#         serializer = ServiceSerializer(services, many=True)

#         response_data = serializer.data
#         status_code = status.HTTP_200_OK

#         return Response(response_data, status_code)


#     def post(self, request):
#         '''Add a new Service visit'''
#         pass


#     def put(self, request):
#         '''Update an existing Service visit'''
#         pass


#     def delete(self, request):
#         '''Delete a Service visit'''
#         pass
