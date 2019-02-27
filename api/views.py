from django.contrib.auth import logout

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.permissions import IsResident


class ResidentProfile(APIView):

    permission_classes = (IsAuthenticated, IsResident)

    def get(self, request):
        '''Return profile information of Resident'''
        print("hello")
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


# class ResidentVehicle(APIView):

#     permission_classes = (IsAuthenticated, IsResident)

#     def get(self, request):
#         '''Return profile information of Resident'''
#         resident = request.user.profile.resident
        

#         response_data = serializer.data
#         status_code = status.HTTP_200_OK
#         return Response(response_data, status_code)


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
        flat = request.user.profile.resident.flat

        data = request.data
        try:
            data = validate_guest_visit_data(data)
        except ValueError:
            response_data = {'message': "Incorrect values or format"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status_code)


        flat.add_guest_visit(data=data)

        response_data = {'message': "Guest added"}
        status_code = status.HTTP_200_OK
        return Response(response_data, status_code)

#     def patch(self, request):
#         '''Update an existing Guest visit to a Resident'''
#         pass


#     def delete(self, request):
#         '''Delete a Guest visit to a Resident'''
#         pass


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
