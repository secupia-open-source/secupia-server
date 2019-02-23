# from __future__ import unicode_literals

# from django.contrib.auth.models import User
# from django.db import models

# class Resident(models.Model):

#     MALE = 'M'
#     FEMALE = 'F'
#     OTHERS = 'O'

#     GENDER = (
#         (MALE, "Male"),
#         (FEMALE, "Female"),
#         (OTHERS, "Others"),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     dob = models.DateField()
#     gender = models.CharField(max_length=1, choices=GENDER, default=MALE)
#     occupation = models.CharField(max_length=100)
#     contact = models.PositiveIntegerField()
#     profile_pic = models.ImageField()
#     license_num = models.CharField(max_length=10)
#     # flat = models.ForeignKey('Flat', on_delete=models.CASCADE)

#     '''
#     From User model: first_name, last_name, email
#     '''

#     def __str__(self):
#         return self.get_name()

#     def get_name(self):
#         return self.user.first_name + self.user.last_name


# class Flat(models.Model):
#     flat_num = models.CharField(max_length=10)
#     owner = models.ForeignKey(Resident, on_delete=models.SET_NULL)

#     def __str__(self):
#         return self.flat_num


# class ParkingSlot(models.Model):
#     slot_num = models.CharField(max_length=10)
#     flat = models.OneToOneField('Flat', on_delete=models.CASCADE)
#     is_guest = models.BooleanField(default=False)

#     def __str__(self):
#         return self.slot_num


# class Guest(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()
#     guest_visit = models.ManyToManyField(GVisit)

#     def __str__(self):
#         return self.get_name()

#      def get_name(self):
#         return self.first_name + self.last_name


# ''' Vehicle Models '''

# class Vehicle(models.Model):
#     license_plate = models.CharField(max_length=10)

#     def __str__(self):
#         return self.slot_num

#     # add get_name


# class ResidentVehicle(models.Model):
#     vehicle = models.OneToOne(Vehicle, on_delete=models.CASCADE)
#     model = models.CharField(max_length=100)
#     resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.slot_num


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


# class Visit(models.Model):
#     purpose = models.CharField(max_length=100)

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return self.slot_num


# class GuestVisit(Visit):
#     guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
#     flat = models.ForeignKey(Flat, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.guest.get_name() + ":" + self.purpose 


# class ServiceVisit(Visit):

#     def __str__(self):
#         return self.slot_num


# ''' Transaction Models '''


# class Transaction(models.Model):
#     date_time = models.DateTimeField(auto_now_add=True)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     is_entry = models.BooleanField(default=True) # Categorize whether 

#     def __str__(self):
#         return vehicle + ":" + date_time


# class ResidentTransaction(models.Model):
#     pass


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

