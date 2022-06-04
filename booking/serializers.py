from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import ValidationError

from booking.models import Booking
from clinician.models import ClinicianAvailability
from clinician.serializers import AvailabilitySerializer
from patient.models import Patient
from patient.serializers import PatientSerializer


class BookingSerializer(serializers.ModelSerializer):
    time_slot_id = serializers.UUIDField(format='hex_verbose', write_only=True)
    patient_id = serializers.UUIDField(format='hex_verbose', write_only=True)
    clinician_availability = AvailabilitySerializer(read_only=True)
    patient = PatientSerializer(read_only=True)


    class Meta:
        model = Booking
        fields = ['clinician_availability', 'patient', 'time_slot_id', 'patient_id', 'status', 'cancellation_reason', 'pk']
        extra_kwargs = {
            'status': {'required': False},
            'pk': {'read_only': True}
        }

    def validate(self, data):
        super().validate(data)
        # The self.instance will differentiate between create flow and update flow.
        if self.instance and not data.get('status', None):
            raise ValidationError('Status is a mandatory field for update')
        if self.instance and data['status'] == Booking.BookingStatus.CANCELLED and not data.get('cancellation_reason', None):
            raise ValidationError('Providing valid reason is mandatory while cancelling booking')
        return data

    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        time_slot_id = validated_data.pop('time_slot_id')
        patient = Patient.objects.get(pk=patient_id)
        with transaction.atomic():
            time_slot = ClinicianAvailability.fetch_available_slot(time_slot_id)
            is_patient_booked = Booking.check_patient_availability(patient_id, time_slot)
            if is_patient_booked:
                raise ValidationError("Patient already has an appointment for the same timeslot")

            return Booking.objects.create(patient=patient, clinician_availability=time_slot, **validated_data)

    def to_representation(self, instance):
        booking_record = super().to_representation(instance)
        booking_record['booking_id'] = booking_record['pk']
        del booking_record['pk']
        if booking_record['status'] != Booking.BookingStatus.CANCELLED:
            del booking_record['cancellation_reason']
        return booking_record
