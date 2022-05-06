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
