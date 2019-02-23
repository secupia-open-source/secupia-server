from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ResidentProfile(APIView):

    def get(self, request):
        '''Return profile information of Resident'''
        resident = Resident.objects.get(user=request.user)
        serializer = ResidentSerializer(resident)

        response_data = serializer.data
        status_code = status.HTTP_200_OK

        return Response(response_data, status_code)


#     def post(self, request):
#         '''Add a new Resident'''
#         request_data = request.data

#         try:
#             val_data = validate_resident_data(request_data)
#         except:
#             pass

#         resident = Resident.objects.create(**val_data)
#         serializer = ResidentSerializer(resident)

#         response_data = serializer.data
#         status_code = status.HTTP_200_OK

#         return Response(response_data, status_code)


#     def patch(self, request):
#         '''Update profile information of Resident'''
#         pass


#     def delete(self, request):
#         '''Delete a Resident'''
#         pass


# class ResidentGuestVisit(APIView):

#     def get(self, request):
#         '''Return all Guest visits for a Resident'''
#         resident = Resident.objects.get(user=request.user)
#         guest_visits = resident.get_guest_visits()
#         serializer = GuestVisitSerializer(guest_visits, many=True)

#         response_data = serializer.data
#         status_code = status.HTTP_200_OK

#         return Response(response_data, status_code)


#     def post(self, request):
#         '''Add a new Guest visit to a Resident'''
#         pass


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
