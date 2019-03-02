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


admin.site.register(models.Society, SocietyAdmin)
admin.site.register(models.Flat)
admin.site.register(models.Owner)
admin.site.register(models.Resident)
admin.site.register(models.Vehicle, VehicleAdmin)
admin.site.register(models.ResidentVehicle)
admin.site.register(models.Guest)
admin.site.register(models.Transaction)
