from django_filters import rest_framework as filters

from booking.models import Booking


class BookingFilter(filters.FilterSet):

    class Meta:
        model = Booking
        fields = ['status', 'cancellation_reason']
