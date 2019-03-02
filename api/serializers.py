from django.contrib.auth.models import User

from rest_framework import serializers

from api import models


class FlatSerializer(serializers.ModelSerializer):
    '''Flat Serializer class'''
    name = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    addr = serializers.SerializerMethodField()

    class Meta:
        model = models.Flat
        fields = ('id', 'name', 'contact', 'addr')

    def get_name(self, obj):
        '''Return address'''
        if obj.owner is not None:
            return obj.owner.name
        else:
            return "Something" # Remove later

    def get_contact(self, obj):
        '''Return address'''
        if obj.owner is not None:
            return obj.owner.contact
        else:
            return 9876543210 # Remove later

    def get_addr(self, obj):
        '''Return serialized society data'''
        return obj.get_address()


class ResidentVehicleSerializer(serializers.ModelSerializer):
    '''Resident Vehicle Serializer class'''
    license_plate = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = models.ResidentVehicle
        fields = ('id', 'license_plate', 'model', 'manufacturer', 
            'status', 'is_locked')

    def get_owner(self, obj):
        '''Return serialized flat data'''
        return obj.owner.profile.name

    def get_license_plate(self, obj):
        '''Return serialized flat data'''
        return obj.vehicle.license_plate

    def get_status(self, obj):
        '''Return serialized flat data'''
        return self.get_status()


class ResidentVehicleTransactionSerializer(serializers.ModelSerializer):
    '''Resident Vehicle Log Serializer class'''
    
    is_entry = serializers.SerializerMethodField()

    class Meta:
        model = models.Transaction
        fields = ('id', 'vehicle', 'date_time', 'is_entry')

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
        fields = ('id', 'name', 'contact', 'flat', 'purpose', 'expected_date_time')

    def get_flat(self, obj):
        '''Return flat address'''        
        return obj.flat.get_address()
