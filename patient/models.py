from django.db import models
from django.contrib.auth import get_user_model

from app.models import AbstractBaseModel


User = get_user_model()


class Patient(AbstractBaseModel):
    #Relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        # The table name as shown in the DB.
        # Default table name is <app_name>_<table_name>
        db_table = "patient"

    def soft_delete(self):
        super().soft_delete()
        self.user.is_active = False
        self.user.save()
