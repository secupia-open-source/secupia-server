from datetime import date

from django.db import models
from django.utils import timezone

from api import models as api_models


class GuestQuerySet(models.QuerySet):
    def get_or_create(cls, **kwargs):
        '''Returns all active guests visits or
        active guest visits for a flat'''
        try:
            flat = kwargs['flat']
            return cls.filter(flat=flat, status=api_models.Visit.ACTIVE)
        except KeyError:
            return cls.filter(status=api_models.Visit.ACTIVE)


class GuestVisitQuerySet(models.QuerySet):
    def active_guest_visits(cls, **kwargs):
        '''Returns all active guests visits or
        active guest visits for a flat'''
        try:
            flat = kwargs['flat']
            return cls.filter(flat=flat, status=api_models.Visit.ACTIVE)
        except KeyError:
            return cls.filter(status=api_models.Visit.ACTIVE)