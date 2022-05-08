from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from booking.models import Booking
from patient.models import Patient
from booking.serializers import BookingSerializer
from patient.serializers import PatientSerializer


class PatientViewset(viewsets.ModelViewSet):
    """
    Viewset to add, view list and view details of patients.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def __get_default_bad_func_message(self, func):
        return {'message': f'{func} function is not offered in this path.'}

    def update(self, request, pk=None):
        default_message = self.__get_default_bad_func_message("PUT")
        return Response(default_message, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        default_message = self.__get_default_bad_func_message("PATCH")
        return Response(default_message, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        patient.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PatientBookingViewset(viewsets.ViewSet):

    def __get_booking_list(self, patient_id):
        return Booking.get_patient_booking_list(patient_id)

    def list(self, request, patient_id):
        queryset = self.__get_booking_list(patient_id)
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, patient_id, booking_id):
        queryset = self.__get_booking_list(patient_id)
        booking = get_object_or_404(queryset, pk=booking_id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def partial_update(self, request, patient_id, booking_id):
        queryset = self.__get_booking_list(patient_id)
        booking = get_object_or_404(queryset, pk=booking_id)
        serializer = BookingSerializer(booking, data=request.data, partial=True, source='partial_update')
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
