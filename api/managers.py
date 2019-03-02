from datetime import date

from django.db import models
from django.utils import timezone

from api import models as api_models


class GuestQuerySet(models.QuerySet):
    def flats_expecting_guests(cls, **kwargs):
        '''Returns all flats expecting guests'''
        flats = []
        for flat in cls.all():
        	if count(flat.get_active_guests()) != 0:
        		flats.append(flat)
        		continue
        return flats