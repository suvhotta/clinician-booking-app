from django.db.models.signals import post_save
from django.dispatch import receiver
from celery.task import task
from celery.utils.log import get_task_logger

from booking.models import Booking
from clinician.models import ClinicianAvailability


logger = get_task_logger(__name__)


@task(name="handle clinician availability")
def async_clinician_availability_handler(availability_id, created):
    instance = ClinicianAvailability.objects.get(pk=availability_id)
    if created:
        instance.is_available = False
        logger.info(f"Clinician: {instance.clinician.user.first_name} got booked!")
    elif instance.status == Booking.BookingStatus.CANCELLED and not created:
        instance.is_available = True
        logger.info(f"Clinician: {instance.clinician.user.first_name} became available!")
    instance.save()


@receiver(post_save, sender=Booking)
def clinician_availability_handler(sender, instance, created, **kwargs):
    async_clinician_availability_handler.delay(instance.clinician_availability_id, created)
