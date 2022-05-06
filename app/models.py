import uuid

from django.db import models


class AbstractBaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(default=False)
    objects = AbstractBaseManager()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True
