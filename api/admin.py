from django.contrib import admin

from api import models

class FlatInLine(admin.TabularInline):
    model = models.Flat
    extra = 0


class SocietyAdmin(admin.ModelAdmin):
    inlines = [FlatInLine]


class TransactionInLine(admin.TabularInline):
    model = models.Transaction
    extra = 0


class VehicleAdmin(admin.ModelAdmin):
    inlines = [TransactionInLine]


class GuestVisitInLine(admin.TabularInline):
    model = models.GuestVisit
    extra = 0


class GuestAdmin(admin.ModelAdmin):
    inlines = [GuestVisitInLine]


class FlatAdmin(admin.ModelAdmin):
    inlines = [GuestVisitInLine]


admin.site.register(models.UserProfile)
admin.site.register(models.Society, SocietyAdmin)
admin.site.register(models.Flat, FlatAdmin)
admin.site.register(models.Resident)
admin.site.register(models.Vehicle, VehicleAdmin)
admin.site.register(models.ResidentVehicle)
admin.site.register(models.Guest, GuestAdmin)
admin.site.register(models.Transaction)
