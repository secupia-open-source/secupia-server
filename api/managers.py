from datetime import date

from django.db import models
from django.utils import timezone

from api import models as api_models


class FlatQuerySet(models.QuerySet):
    def flats_expecting_guests(cls, **kwargs):
        '''Returns all flats expecting guests'''
        flats = []
        for flat in cls.all():
        	if flat.get_active_guests().exists():
        		flats.append(flat)
        		continue
        return flats


class VehicleQuerySet(models.QuerySet):
    def get_recent(cls, **kwargs):
        '''Returns most recent transaction'''
        transactions = api_models.Transaction.objects.all().order_by('-timestamp')
        if transactions.exists():
        	return transactions[0]
        else:
            return None