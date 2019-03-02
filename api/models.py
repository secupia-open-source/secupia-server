from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from api import managers


class Society(models.Model):
    '''Society model class'''
    name = models.CharField(max_length=100)

    # flats: Flat

    class Meta:
        verbose_name_plural = "Societies"

    def __str__(self):
        return "Society: {}".format(self.name)

    def __repr__(self):
        ret_string = 'Society(name="{}")'.format(self.name)
        return ret_string


class Flat(models.Model):
    '''Flat model class'''
    user = models.OneToOneField(User, related_name='flat', 
        on_delete=models.CASCADE) # User for owner and resident
    name = models.CharField(max_length=10)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    owner = models.ForeignKey('Owner', on_delete=models.SET_NULL, null=True, blank=True)
    landline = models.PositiveIntegerField(default=None, null=True)

    # guests: Guest
    # registration_tokens: RegistrationToken
    # parking_slot: ParkingSlot

    objects = managers.FlatQuerySet.as_manager()

    class Meta:
        default_related_name = "flats"

    def __str__(self):
        return "Flat: {}, {}".format(self.society, self.name)

    def __repr__(self):
        ret_string = 'Flat(flat="{}", society="{}")'.format(
                        self.name,
                        self.society
                    )
        return ret_string

    def get_address(self):
        return "{}: {}".format(self.name, self.society)

    def get_active_guests(self):
        return self.guests.filter(is_active=True)

    def add_guest(self, val_data):
        val_data['flat'] = self
        guest = Guest.objects.create(**val_data)
        return guest.id

    def get_vehicles(self):
        vehicles = []
        for resident in self.residents.all():
            vehicles.extend(resident.vehicles.all())
        return vehicles


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


class Owner(UserProfile):
    '''Owner model class'''
    email = models.EmailField()
    dob = models.DateField()
    occupation = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    license_num = models.CharField(max_length=10, null=True)

    # flats: Flat

    def __str__(self):
        ret_string = "Owner: {}, Flats: ".format(self.name)
        for flat in self.flats.all():
            ret_string += flat.get_address() + ", "
        return ret_string

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
        default_related_name = "residents"

    def __str__(self):
        return "Resident: {}".format(self.name)

    def __repr__(self):
        ret_string = 'Resident(name="{}", flat="{}")'.format(
                        self.name,
                        # self.gender,
                        # self.contact,
                        # self.email,
                        self.flat.name
                    )
        return ret_string

    def get_active_guest_visits(self):
        return GuestVisit.objects.active_guest_visits(flat=self.flat)

    def get_addr(self):
        return "{}, {}".format(self.flat.flat, self.flat.society.name)


class Guest(UserProfile):
    '''Guest model class'''
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    purpose = models.TextField()
    expected_date_time = models.DateTimeField(null=True, blank=True)
    expected_duration_of_stay = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_by_guard = models.BooleanField(default=False)
    is_quick_service = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    vehicle = models.ForeignKey('GuestVehicle', null=True, on_delete=models.SET_NULL)

    class Meta:
        default_related_name = "guests"

    def __str__(self):
        return self.name

    def __repr__(self):
        ret_string = 'Guest(name={}, flat={}, purpose={}, is_active={}, is_by_guard={})'.format(
                        self.name
                    )
        return ret_string

    def get_name(self):
        return self.name

    def set_vehicle(license_plate):
        self.vehicle = GuestVehicle.objects.get(vehicle__license_plate=license_plate)


class ParkingSlot(models.Model):
    name = models.CharField(max_length=10)
    is_guest = models.BooleanField(default=False)

    # flat: Flat

    def __str__(self):
        ret_string = "{}: ".format(self.name)
        if self.is_guest:
            ret_string += ": Guest"
        else:
            ret_string += ": {}".format(self.flat)
        return ret_string

    def __repr__(self):
        ret_string = 'ParkingSlot(name={}, is_guest={})'.format(
                        self.name,
                        self.is_guest
                    )
        return ret_string


class Vehicle(models.Model):
    '''Vehicle model class'''
    '''Development Notes:
    Split license_plate into factors
    '''
    license_plate = models.CharField(max_length=13, unique=True)

    objects = managers.VehicleQuerySet.as_manager()

    def __str__(self):
        return "Vehicle {}".format(self.license_plate)

    def __repr__(self):
        ret_string = 'Vehicle(license_plate={})'.format(license_plate)
        return ret_string

    @property
    def is_resident_vehicle(self):
        try:
            resident_vehicle = self.resident_vehicle
            if resident_vehicle.id:
                return True
        except (AttributeError, Vehicle.resident_vehicle.RelatedObjectDoesNotExist):
            return False

    @property
    def is_guest_vehicle(self):
        try:
            guest_vehicle = self.guest_vehicle
            if guest_vehicle.id:
                return True
        except (AttributeError, Vehicle.guest_vehicle.RelatedObjectDoesNotExist):
            return False

    def add_transaction(self, is_entry):
        transaction = Transaction.objects.create(vehicle=self, is_entry=is_entry)
        return transaction

    def get_status(self):
        transactions = self.transactions.all().order_by('-timestamp')
        if transactions.exists():
            latest_tranasction = transactions[0]
            if latest_tranasction.is_entry:
                return 'In'
            else:
                return 'Out'
        else:
            return 'In'


class ResidentVehicle(models.Model):
    '''Resident Vehicle model class'''
    vehicle = models.OneToOneField(Vehicle, related_name="resident_vehicle", on_delete=models.CASCADE)
    owner = models.ForeignKey(Resident, related_name="vehicles", on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    is_locked = models.BooleanField(default=True) # Smart Lock

    def __str__(self):
        return 'Owner: {}, Vehicle: "{}", Model: {}, {}'.format(self.owner.name, self.vehicle.license_plate,
            self.model, self.manufacturer)

    def __repr__(self):
        ret_string = 'ResidentVehicle(vehicle={}, owner={}, model="{}", manufacturer="{}")'.format(
                        self.vehicle,
                        self.owner,
                        self.model,
                        self.manufacturer
                    )
        return ret_string


class GuestVehicle(models.Model):
    '''Guest Vehicle model class'''
    vehicle = models.OneToOneField(Vehicle, related_name="guest_vehicle", on_delete=models.CASCADE)

    def __str__(self):
        return "Guest vehicle {}".format(self.vehicle)

    def __repr__(self):
        ret_string = 'GuestVehicle(vehicle={})'.format(self.vehicle)
        return ret_string


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
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


class RegistrationToken(models.Model):
    '''Registration Token model class'''
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    registration_token = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        default_related_name = "registration_tokens"

    def __str__(self):
        return "Registration token {} for {}".format(
                self.registration_token[:10],
                self.flat.__str__()
            )

    def __repr__(self):
        ret_string = 'RegistrationToken(flat="{}", registration_token="{}")'.format(
                        self.flat.address,
                        self.registration_token[:10]
                    )
        return ret_string


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

