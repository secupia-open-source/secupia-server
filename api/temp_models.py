from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from api import managers


class Society(models.Model):
    '''Society model class'''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Societies"

    def __str__(self):
        return "Society: {}".format(self.name)

    def __repr__(self):
        ret_string = 'Society(name="{}")'.format(self.name)
        return ret_string


class Flat(models.Model):
    '''Flat model class'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=10)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    owner = models.ForeignKey('Owner', on_delete=models.SET_NULL, null=True)
    registration_token = models.ForeignKey('RegistrationToken', null=True, blank=True)

    class Meta:
        default_related_name = "flats"

    def __str__(self):
        return "Flat: {}, {}".format(self.society, self.flat)

    def __repr__(self):
        ret_string = 'Flat(flat="{}", society="{}", owner="{}")'.format(
                        self.flat,
                        self.society,
                        self.owner
                    )
        return ret_string

    def add_guest_visit(self, guest_data, visit_data):
        from pprint import pprint
        pprint(guest_data)
        guest = Guest.objects.get_or_create(**guest_data)

        visit_data['guest'] = guest
        visit_data['flat'] = self
        
        GuestVisit.objects.add(**visit_data)


class UserProfile(models.Model):
    '''User Profile model class'''
    MALE = 'M'
    FEMALE = 'F'
    OTHERS = 'O'

    GENDER = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHERS, "Others"),
    )

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER, null=True)
    contact = models.PositiveIntegerField()

    class Meta:
        abstract = True


class RegistrationToken(models.Model):
    '''Registration Token model class'''
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    registration_token = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "Registration token {} for {}".format(
                self.registration_token[:10],
                self.flat.__str__()
            )

    def __repr__(self):
        ret_string = 'RegistrationToken(flat="{}", registration_token="{}")'.format(
                        self.flat.address,
                        self.registration_token
                    )
        return ret_string


class Owner(UserProfile):
    '''Owner model class'''
    email = models.EmailField()
    dob = models.DateField()
    occupation = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    license_num = models.CharField(max_length=10, null=True)

    # flats: Flat

    class Meta:
        default_related_name = "resident"

    def __str__(self):
        return "Resident: {}".format(self.profile.name)

    def __repr__(self):
        ret_string = 'Owner(user="{}", flat="{}")'.format(
                        self.profile,
                        self.flat
                    )
        return ret_string


class Resident(UserProfile):
    '''Resident model class'''
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    email = models.EmailField()
    dob = models.DateField()
    occupation = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    license_num = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        default_related_name = "resident"

    def __str__(self):
        return "Resident: {}".format(self.profile.name)

    def __repr__(self):
        ret_string = 'Resident(user="{}", flat="{}")'.format(
                        self.profile,
                        self.flat
                    )
        return ret_string

    def get_active_guest_visits(self):
        return GuestVisit.objects.active_guest_visits(flat=self.flat)

    def get_addr(self):
        return "{}, {}".format(self.flat.flat, self.flat.society.name)


class Guest(UserProfile):
    '''Guest model class'''
    flat = models.ForeignKet(Flat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    purpose = models.TextField()

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        ret_string = 'Guest(user={})'.format(
                        self.profile
                    )
        return ret_string

    def get_name(self):
        return self.profile.name


class Vehicle(models.Model):
    '''Vehicle model class'''
    '''Development Notes:
    Split license_plate into factors
    '''
    license_plate = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return "Vehicle: {}".format(self.license_plate)

    def __repr__(self):
        ret_string = 'Vehicle(license_plate={})'.format(license_plate)

    @property
    def is_resident_vehicle(self):
        try:
            resident_vehicle = self.resident_vehicle
            if resident_vehicle.id:
                return True
        except (AttributeError, Vehicle.resident_vehicle.RelatedObjectDoesNotExist):
            return False

    # @property
    # def is_guest_vehicle(self):
    #     try:
    #         guest_vehicle = self.guest_vehicle
    #         if guest_vehicle.id:
    #             return True
    #     except (AttributeError, Vehicle.guest_vehicle.RelatedObjectDoesNotExist):
    #         return False

    # @property
    # def is_service_vehicle(self):
    #     try:
    #         service_vehicle = self.service_vehicle
    #         if service_vehicle.id:
    #             return True
    #     except (AttributeError, Vehicle.service_vehicle.RelatedObjectDoesNotExist):
    #         return False

    def add_transaction(self, is_entry):
        transaction = Transaction.objects.create(vehicle=self, is_entry=is_entry)

        # if self.is_resident:
            # self.send_notification(transa)


    def send_notification(self, transaction):
        if not isinstance(transaction, Transaction):
            raise ValueError

        if self.is_resident_vehicle:
            resident = self.resident_vehicle.owner
            sendNotification(resident.registration_token, transaction)


class ResidentVehicle(models.Model):
    '''Resident Vehicle model class'''
    vehicle = models.OneToOneField(Vehicle, related_name="resident_vehicle", on_delete=models.CASCADE)
    owner = models.ForeignKey(Resident, related_name="vehicles", on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return "{}, {}".format(self.owner, self.vehicle)

    def __repr__(self):
        ret_string = 'ResidentVehicle(vehicle={}, owner={}, model="{}", manufacturer="{}")'.format(
                        self.vehicle,
                        self.owner,
                        self.model,
                        self.manufacturer
                    )


class ResidentVehicle(models.Model):
    '''Resident Vehicle model class'''
    vehicle = models.OneToOneField(Vehicle, related_name="resident_vehicle", on_delete=models.CASCADE)
    owner = models.ForeignKey(Resident, related_name="vehicles", on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return "{}, {}".format(self.owner, self.vehicle)

    def __repr__(self):
        ret_string = 'ResidentVehicle(vehicle={}, owner={}, model="{}", manufacturer="{}")'.format(
                        self.vehicle,
                        self.owner,
                        self.model,
                        self.manufacturer
                    )


class Transaction(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    vehicle = models.ForeignKey(Vehicle, related_name="transactions", on_delete=models.CASCADE)
    is_entry = models.BooleanField(default=True)

    def __str__(self):
        if self.is_entry:
            return "{}, date&time: {}, {}".format(self.vehicle, self.date_time, "Entry")
        else:
            return "{}, date&time: {}, {}".format(self.vehicle, self.date_time, "Exit")            

    def __repr__(self):
        ret_string = 'Transaction(vehicle={}, date_time={}, is_entry={})'.format(
                        self.vehicle,
                        self.date_time,
                        self.is_entry
                    )


class Visit(models.Model):
    '''Visit model class'''
    PASSIVE = 'P'
    ACTIVE = 'A'

    STATUS = (
        (PASSIVE, "Passive"),
        (ACTIVE, "Active"),
    )

    purpose = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True) # Change field_name to timestamp
    status = models.CharField(max_length=1, choices=STATUS, default=ACTIVE)

    class Meta:
        abstract = True


# class ParkingSlot(models.Model):
#     slot_num = models.CharField(max_length=10)
#     flat = models.OneToOneField('Flat', on_delete=models.CASCADE)
#     is_guest = models.BooleanField(default=False)

#     def __str__(self):
#         return self.slot_num




# ''' Vehicle Models '''


# class GuestVehicle(Vehicle):
#     vehicle = models.OneToOne(Vehicle, on_delete=models.CASCADE)
#     guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.slot_num


# class ServiceVehicle(Vehicle):
#     vehicle = models.OneToOne(Vehicle, on_delete=models.CASCADE)
#     guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.slot_num


# ''' Visit Models '''


# class ServiceVisit(Visit):

#     def __str__(self):
#         return self.slot_num


# ''' Transaction Models '''




# class GuestTransaction(models.Model):
#     pass


# class ServiceTransaction(models.Model):
#     pass

# class RegisteredGuest(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     flat = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
#     purpose = models.CharField(max_length=250)
#     guest_visit = models.ManyToManyField(GVisit)


# class Security(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     company = models.CharField(max_length=200)
#     entry = models.CharField(max_length=10)
#     exit = models.CharField(max_length=10)


# class Service(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     job_profile = models.CharField(max_length=200)
#     service_visit = models.ManyToManyField(SVisit)


# class ServiceVehicle(models.Model):
#     organisation = models.CharField(max_length=200)
#     inTime = models.ForeignKey(Transactions)
#     outTime = models.ForeignKey(Transactions)

