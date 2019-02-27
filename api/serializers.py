from django.contrib.auth.models import User

from rest_framework import serializers

from api import models


class UserSerializer(serializers.ModelSerializer):
    '''User serializer class'''
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    '''User Profile Serializer class'''
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = models.UserProfile
        fields = ('id', 'user', 'name', 'gender', 'contact', 'dob', 
            'occupation',  'license_num')

    def get_user(self, obj):
        '''Return serialized user data'''
        if obj.is_resident:
            user_serializer = UserSerializer(obj.user)
            return user_serializer.data
        else:
            return {}


class SocietySerializer(serializers.ModelSerializer):
    '''Society Serializer class'''
    class Meta:
        model = models.Society
        fields = ('id', 'name')


class FlatSerializer(serializers.ModelSerializer):
    '''Flat Serializer class'''
    society = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = models.Flat
        fields = ('id', 'flat', 'society', 'owner')

    def get_society(self, obj):
        '''Return serialized society data'''
        society_serializer = SocietySerializer(obj.society)
        return society_serializer.data

    def get_owner(self, obj):
        '''Return serialized owner data'''
        owner_serializer = UserProfileSerializer(obj.owner)
        return owner_serializer.data


class ResidentSerializer(serializers.ModelSerializer):
    '''Resident Serializer class'''
    name = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    occupation = serializers.SerializerMethodField()
    license_num = serializers.SerializerMethodField()
    addr = serializers.SerializerMethodField()

    class Meta:
        model = models.Resident
        fields = ('id', 'name', 'gender', 'contact', 'dob', 
            'occupation',  'license_num', 'addr')

    def get_name(self, obj):
        '''Return address'''
        return obj.profile.name
    def get_gender(self, obj):
        '''Return address'''
        return obj.profile.get_gender_display()
    def get_contact(self, obj):
        '''Return address'''
        return obj.profile.contact
    def get_dob(self, obj):
        '''Return address'''
        return obj.profile.dob
    def get_occupation(self, obj):
        '''Return address'''
        return obj.profile.occupation
    def get_license_num(self, obj):
        '''Return address'''
        return obj.profile.license_num
    def get_addr(self, obj):
        '''Return address'''
        return obj.get_addr()


class ResidentVehicleSerializer(serializers.ModelSerializer):
    '''Resident Vehicle Serializer class'''
    license_plate = serializers.SerializerMethodField()
    
    class Meta:
        model = models.ResidentVehicle
        fields = ('id', 'license_plate', 'model', 'manufacturer')

    def get_owner(self, obj):
        '''Return serialized flat data'''
        return obj.owner.profile.name

    def get_license_plate(self, obj):
        '''Return serialized flat data'''
        return obj.vehicle.license_plate


class ResidentVehicleLogSerializer(serializers.ModelSerializer):
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
    profile = serializers.SerializerMethodField()

    class Meta:
        model = models.Guest
        fields = ('id', 'profile')

    def get_profile(self, obj):
        '''Return serialized profile data'''
        profile_serializer = UserProfileSerializer(obj.profile)
        return profile_serializer.data


class VisitSerializer(serializers.ModelSerializer):
    '''Guest Serializer class'''
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        '''Return serialized profile data'''
        return obj.get_status_display()


class GuestVisitSerializer(GuestSerializer, VisitSerializer):
    '''Guest Visit Serializer class'''
    profile = serializers.SerializerMethodField()

    class Meta:
        model = models.GuestVisit
        fields = ('id', 'profile', 'purpose', 'date_time', 'status')

    def get_profile(self, obj):
        '''Return serialized profile data'''
        profile_serializer = UserProfileSerializer(obj.guest.profile)
        return profile_serializer.data



