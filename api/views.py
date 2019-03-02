from firebase_admin import firestore, messaging

from django.contrib.auth import logout

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.models import Guest, Vehicle
from api.permissions import IsFlat
from api.utils import validate_vehicle_log_data, validate_guest_visit_data


class ResidentProfile(APIView):

    permission_classes = (IsAuthenticated, IsFlat)

    def get(self, request):
        '''Return profile information of Resident'''
        flat = request.user.flat
        vehicles = flat.get_vehicles()

        flat_serializer = serializers.FlatSerializer(flat)
        vehicle_serializer = serializers.ResidentVehicleSerializer(vehicles, many=True)

        response_data = {
            "profile": flat_serializer.data,
            "vehicle": vehicle_serializer.data
        }
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class ResidentGuestVisit(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''Return all Guest visits for a Resident'''
        flat = request.user.flat

        guest_visits = flat.get_active_guests()
        serializer = serializers.GuestSerializer(guest_visits, many=True)

        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


    def post(self, request):
        '''Add a new Guest visit to a Resident'''
        '''Development Notes:
        add expected_date_time field
        '''
        flat = request.user.flat

        try:
            val_data = validate_guest_visit_data(request.data)
        except ValueError:
            response_data = {'message': "Invalid request"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)

        guest_id = flat.add_guest(val_data)

        response_data = {
            'message': "Guest added",
            'id': guest_id
        }
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)

    def patch(self, request):
        '''Update an existing Guest visit to a Resident'''
        data = request.data
        try:
            guest = Guest.objects.get(id=data['guest_id'])
            val_data = validate_guest_visit_data(request.data)
        except Guest.DoesNotExist:
            response_data = {'message': "Guest does not exist"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response_data, status_code)
        except ValueError:
            response_data = {'message': "Invalid format or fields may be missing"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)

        guest.name = val_data['name']
        guest.contact = val_data['contact']
        guest.purpose = val_data['purpose']
        # guest.expected_date_time = val_data['expected_date_time']
        guest.save()

        response_data = {'message': "Guest updated"}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


    def delete(self, request):
        '''Delete a Guest visit to a Resident'''
        try:
            guest = Guest.objects.get(id=request.data['guest_id'])
        except Guest.DoesNotExist:
            response_data = {'message': "Guest does not exist"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response_data, status_code)
        
        guest.delete()
        # Override delete function to check if guest is active before deleting

        response_data = {'message': "Guest deleted"}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class ResidentVehicleTransactions(APIView):

    permission_classes = (IsAuthenticated, IsFlat)

    def get(self, request, vehicle_id):
        '''Return profile information of Resident'''
        flat = request.user.flat
        
        vehicles = flat.get_vehicles()
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Check if vehicle belongs to current flat
        if vehicle.resident_vehicle not in vehicles:
            response_data = {'message': "Invalid Request"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)

        serializer = serializers.ResidentVehicleTransactionSerializer(
            vehicle.transactions, many=True)

        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


# class VehicleTransaction(APIView):

#     permission_classes = (IsAuthenticated,)

#     def sendNotification(self, registration_token, transaction):
#         title = 'Order {}'.format(order_status)

#         if is_entry:
#             body = "Your vehicle {} has entered"
#         else:
#             body = "Your vehicle {} has exited"
#         body.format(transaction.vehicle.license_plate)

#         message = messaging.Message(
#             notification = messaging.Notification(
#                 title = title,
#                 body = body,
#             ),
#             token = registration_token,
#         )

#         try:
#             response = messaging.send(message)
#             print(response)
#         except Exception as e:
#             print(e)

#     def post(self, request):
#         '''Add vehicle transaction and send notification to resident'''
#         data = request.data
#         print(data)
#         try:
#             license_plate, is_entry, reg_token = validate_vehicle_log_data(data)
#         except ValueError:
#             response_data = {'message': 'Invalid request'}
#             status_code = status.HTTP_400_BAD_REQUEST
#             return Response(response_data, status_code)
#         except Exception as e:
#             print(e)
#         vehicle, _ = Vehicle.objects.get_or_create(license_plate=license_plate)
#         transaction = vehicle.add_transaction(is_entry)

#         # vehicle.send_notification(reg_token, transaction)

#         response_data = {'message': 'Transaction added'}
#         status_code = status.HTTP_200_OK
#         return Response(response_data, status_code)

