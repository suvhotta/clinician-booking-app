from django.db import models

from app.models import AbstractBaseModel
from clinician.models import ClinicianAvailability
from patient.models import Patient


class Booking(AbstractBaseModel):

    class Meta:
        # The table name as shown in the DB.
        # Default table name is <app_name>_<table_name>
        db_table = "booking"

    class BookingStatus(models.TextChoices):
        CANCELLED = 'CANCELLED'
        PENDING = 'PENDING'
        COMPLETED = 'COMPLETED'

    # Relationship
    clinician_availability = models.ForeignKey(ClinicianAvailability, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    #Fields
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    cancellation_reason = models.CharField(max_length=250, blank=True)

    @staticmethod
    def get_clinician_booking_list(clinician_id):
        return Booking.objects.filter(clinician_availability__clinician__pk=clinician_id)

    @staticmethod
    def get_patient_booking_list(patient_id):
        return Booking.objects.filter(patient__pk=patient_id)

    @staticmethod
    def check_patient_availability(patient_id, timeslot):
        return Booking.objects.filter(
            clinician_availability__start_time=timeslot.start_time,
            patient_id=patient_id,
            status=Booking.BookingStatus.PENDING
        ).first()
