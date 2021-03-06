from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from booking.models import Booking
from booking.serializers import BookingSerializer
from clinician.models import Clinician, ClinicianAvailability
from clinician.serializers import ClinicianSerializer, AvailabilitySerializer
from clinician.filters import ClinicianAvailabilityFilter


class ClinicianViewset(viewsets.ModelViewSet):
    """
    Viewset to add, view list and view details of clinicians.
    """
    queryset = Clinician.objects.all()
    serializer_class = ClinicianSerializer


class ClinicianAvailabilityViewset(viewsets.ModelViewSet):
    """
    Viewset to add, view list and view details of clinicians' availabilities.
    """
    serializer_class = AvailabilitySerializer
    filterset_class = ClinicianAvailabilityFilter

    def get_queryset(self, clinician_id):
        return self.filter_queryset(queryset=ClinicianAvailability.get_clinician_slots(clinician_id))

    def list(self, request, clinician_id):
        queryset = self.get_queryset(clinician_id)
        serializer = AvailabilitySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, clinician_id, availability_id):
        queryset = self.get_queryset(clinician_id)
        available_slot = get_object_or_404(queryset, pk=availability_id)
        serializer = AvailabilitySerializer(available_slot)
        return Response(serializer.data)

    def create(self, request, clinician_id):
        request.data['clinician_id'] = clinician_id
        serializer = AvailabilitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookClinicianAvailabilityViewset(viewsets.ViewSet):
    """
    Viewset to book a clinician's available slot and list down the appointments of a clinician.
    """
    def create(self, request, clinician_id):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, clinician_id):
        queryset = Booking.get_clinician_booking_list(clinician_id)
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)
