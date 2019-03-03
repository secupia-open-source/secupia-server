from django.contrib.auth.models import User

from rest_framework import serializers

from api import models


class FlatSerializer(serializers.ModelSerializer):
    '''Flat Serializer class'''
    short_addr = serializers.SerializerMethodField()
    addr = serializers.SerializerMethodField()

    class Meta:
        model = models.Flat
        fields = ('id', 'short_addr', 'addr', 'landline')

    def get_short_addr(self, obj):
        '''Return serialized society data'''
        return obj.name

    def get_addr(self, obj):
        '''Return serialized society data'''
        return obj.get_address()


class ResidentVehicleSerializer(serializers.ModelSerializer):
    '''Resident Vehicle Serializer class'''
    id = serializers.SerializerMethodField()
    license_plate = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = models.ResidentVehicle
        fields = ('id', 'license_plate', 'model', 'manufacturer', 
            'status', 'is_locked')

    def get_id(self, obj):
        '''Return serialized flat data'''
        return obj.vehicle.id

    def get_owner(self, obj):
        '''Return serialized flat data'''
        return obj.owner.profile.name

    def get_license_plate(self, obj):
        '''Return serialized flat data'''
        return obj.vehicle.license_plate

    def get_status(self, obj):
        '''Return serialized flat data'''
        return obj.vehicle.get_status()


class VehicleTransactionSerializer(serializers.ModelSerializer):
    '''Vehicle transaction Serializer class'''
    
    is_entry = serializers.SerializerMethodField()

    class Meta:
        model = models.Transaction
        fields = ('id', 'vehicle', 'timestamp', 'is_entry')

    def is_entry(self, obj):
        if obj.is_entry:
            return "Entry"
        else:
            return "Exit"


class GuestSerializer(serializers.ModelSerializer):
    '''Guest Serializer class'''
    flat = serializers.SerializerMethodField()

    class Meta:
        model = models.Guest
        fields = ('id', 'name', 'contact', 'flat', 'purpose', 
            'expected_date_time', 'expected_duration_of_stay')

    def get_flat(self, obj):
        '''Return flat address'''        
        return obj.flat.get_address()
