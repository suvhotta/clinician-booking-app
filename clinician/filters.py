import django_filters
from django_filters import rest_framework as filters
from django.db import models as django_models

from clinician.models import ClinicianAvailability


class ClinicianAvailabilityFilter(filters.FilterSet):

    class Meta:
        model = ClinicianAvailability
        fields = {
            'is_available': ('exact', ),
            'start_time': ('lte', 'gte'),
            'end_time': ('lte', 'gte'),
        }
        # fields = ['is_available', 'start_time_gte']

    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': django_filters.DateTimeFilter
        },
    }
