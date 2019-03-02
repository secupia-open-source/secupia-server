from firebase_admin import firestore, messaging

from django.contrib.auth import logout

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.models import Flat, Guest, Vehicle
from api.permissions import IsFlat
from api.utils import validate_vehicle_log_data, validate_guest_visit_data


class VehicleTransaction(APIView):

    permission_classes = (IsAuthenticated,)

    def sendNotification(self, registration_token, transaction):
        title = "Car log"

        if transaction.is_entry:
            body = "Your vehicle {} has entered"
        else:
            body = "Your vehicle {} has exited"
        body = body.format(transaction.vehicle.license_plate)

        message = messaging.Message(
            notification = messaging.Notification(
                title = title,
                body = body,
            ),
            token = registration_token,
        )

        try:
            response = messaging.send(message)
            print("Response: ", response)
        except Exception as e:
            print("Error: ", e)

    def post(self, request):
        '''Add vehicle transaction and send notification to resident'''
        data = request.data
        try:
            license_plate, is_entry = validate_vehicle_log_data(data)
        except ValueError:
            response_data = {'message': 'Invalid request'}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)

        vehicle, _ = Vehicle.objects.get_or_create(license_plate=license_plate)
        transaction = vehicle.add_transaction(is_entry)

        flat = request.user.flat
        for reg_token in flat.registration_tokens.all():
            self.sendNotification(reg_token, transaction)

        response_data = {'message': 'Transaction added'}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class FlatVehicles(APIView):

    permission_classes = (IsAuthenticated, IsFlat)

    def get(self, request):
        '''Return list of vehicles registered for a flat'''
        flat = request.user.flat
        vehicles = flat.get_vehicles()
        serializer = serializers.ResidentVehicleSerializer(vehicles, many=True)

        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class FlatVehicleTransactions(APIView):

    permission_classes = (IsAuthenticated, IsFlat)

    def get(self, request, vehicle_id):
        '''Return all transactions for a vehicle'''
        flat = request.user.flat
        
        # Get all vehicles for current flat
        vehicles = flat.get_vehicles()

        # Get vehicle in request
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Check if request vehicle belongs to current flat
        if vehicle.resident_vehicle not in vehicles:
            response_data = {'message': "Invalid Request"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)

        serializer = serializers.VehicleTransactionSerializer(
            vehicle.transactions, many=True)

        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class FlatGuest(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''Return all guests a flat is expecting'''
        flat = request.user.flat
        guest_visits = flat.get_active_guests()
        serializer = serializers.GuestSerializer(guest_visits, many=True)

        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


    def post(self, request):
        '''Add a new guest'''
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
        '''Update a guest expected by a flat'''
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
        '''Delete an expected guest'''
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


class SmartLockView(APIView):

    permission_classes = (IsAuthenticated, IsFlat,)

    def post(self, request):
        '''Update smart lock of vehicle'''
        flat = request.user.flat
        
        # Get all vehicles for current flat
        vehicles = flat.get_vehicles()

        # Get vehicle in request
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Check if request vehicle belongs to current flat
        if vehicle.resident_vehicle not in vehicles:
            response_data = {'message': "Invalid Request"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)

        # Update vehicle's smart lock
        vehicle.is_locked = not(vehicle.is_locked)
        vehicle.save()

        response_data = {'message': "Request Successful"}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class FlatView(APIView):

    # permission_classes = (IsAuthenticated,) # Thank Nishant

    def get(self, request):
        # TO BE IMPLEMENTED # Courtesy Nishant, ignored now
        # society = request.user.get_society() 
        # flats = Flat.objects.filter(society=society)
        
        flats = Flat.objects.all()
        serializer = serializers.FlatSerializer(flats, many=True)
        
        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class FlatsExpectingGuestsView(APIView): # Give better Name

    # permission_classes = (IsAuthenticated,) # Thank Nishant

    def get(self, request):
        '''Return list of flats which are expecting guests'''
        flats = Flat.objects.flats_expecting_guests()
        serializer = serializers.FlatSerializer(flats, many=True)
        
        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)


class GuestsForFlatView(APIView): # Please, give better name

    # permission_classes = (IsAuthenticated,) # Thank Nishant

    def get(self, request, flat_id):
        '''Return list of expected guests for a flat'''
        flat = Flat.objects.get(id=flat_id)
        guests = flat.get_active_guests()
        serializer = serializers.GuestSerializer(guests, many=True)
        
        response_data = serializer.data
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)

    def patch(self, request, flat_id):
        '''Update vehicle for an expected guest'''
        # Get active guests for current flat
        flat = Flat.objects.get(id=flat_id)
        guests = flat.get_active_guests()

        # Get current guest
        try:
            val_data = validate_guard_guest_data(request.data)
        except ValueError:
            response_data = {'message': "Invalid request"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)
            
        # Check if current guest is an active guest of current flat
        guest = Guest.objects.get(id=val_data['guest_id'])
        if guest not in guests:
            response_data = {'message': "Invalid request"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response_data, status_code)

        # Update guest's vehicle
        guest.set_vehicle(val_data['license_num'])
        guest.save()

        response_data = {'message': "Request successful"}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)







# class SmartLock(APIView):

#     permission_classes = (IsAuthenticated, IsFlat)

#     def get(self, request):
#         pass

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

