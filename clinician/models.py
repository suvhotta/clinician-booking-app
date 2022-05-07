from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

from app.models import AbstractBaseModel


User = get_user_model()


class Clinician(AbstractBaseModel):
    # Relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Fields
    degree_conferred_date = models.DateField()
    specializations = ArrayField(models.CharField(max_length=50))


# class AvailabilityManager(models.Manager):
#
#     def get_queryset(self):
#         return super().get_queryset().filter(is_available=True)


class ClinicianAvailability(AbstractBaseModel):
    # Relationships
    # ManyToOne Relationship with Clinician.
    clinician = models.ForeignKey(Clinician, on_delete=models.CASCADE)
    # Fields
    is_available = models.BooleanField(blank=False, default=True)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)

    class Meta:
        db_table = "clinician_availability"

    @staticmethod
    def get_clinician_slots(clinician_id):
        return ClinicianAvailability.objects.filter(clinician__pk=clinician_id)
