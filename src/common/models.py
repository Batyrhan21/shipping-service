import uuid
import random
import string
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("ID"),
    )
    is_deleted = models.BooleanField(default=False, verbose_name=_("удаленный?"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("дата изменения"))

    class Meta:
        abstract = True


class UniqueTruckNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6
        kwargs["unique"] = True
        super().__init__(*args, **kwargs)

    def generate_car_number(self):
        number = random.randint(1000, 9999)
        letter = random.choice(string.ascii_uppercase)
        return f"{number}{letter}"

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = self.generate_car_number()
            setattr(model_instance, self.attname, value)
        return value
