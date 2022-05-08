from django.db.models.signals import post_save
from django.dispatch import receiver

from booking.models import Booking


@receiver(post_save, sender=Booking)
def clinician_availability_handler(sender, instance, created, **kwargs):
    if created:
        instance.clinician_availability.is_available = False
    elif instance.status == Booking.BookingStatus.CANCELLED and not created:
        instance.clinician_availability.is_available = True
    instance.clinician_availability.save()
