import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

from common.models import BaseModel, UniqueTruckNumberField


class Shipment(BaseModel):
    pick_up = models.ForeignKey(
        "service.Location",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="shipment_pickups",
        verbose_name=_("Локация (Pick Up)"),
    )
    delivery = models.ForeignKey(
        "service.Location",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="shipment_deliveries",
        verbose_name=_("Доставка"),
    )
    weight = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(1000)],
        verbose_name="Вес (1-1000)",
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))

    def __str__(self):
        return f"{self.description}"

    class Meta:
        db_table = "service_shipment"
        verbose_name = "Груз"
        verbose_name_plural = "Грузы"
        ordering = ("-created_at",)


class Truck(BaseModel):
    number = UniqueTruckNumberField(null=True, blank=True, verbose_name="Номер")
    curr_location = models.ForeignKey(
        "service.Location",
        on_delete=models.CASCADE,
        related_name="trucks",
        null=True,
        blank=True,
        verbose_name=_("Текущая локация"),
    )
    load_capacity = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(1000)],
        verbose_name="Грузоподъемность (1-1000)",
    )

    def __str__(self) -> str:
        return f"{self.curr_location} - {self.number}"

    def save(self, *args, **kwargs):
        locations = Location.objects.filter(is_deleted=False)
        random_location = random.choice(locations)
        self.curr_location = random_location
        super().save(*args, **kwargs)

    class Meta:
        db_table = "service_truck"
        verbose_name = _("Машина")
        verbose_name_plural = _("Машины")


class Location(BaseModel):
    city = models.CharField(
        max_length=100, blank=False, null=False, verbose_name=_("Город")
    )
    state = models.CharField(
        max_length=100, blank=False, null=False, verbose_name=_("Штат")
    )
    zip_code = models.CharField(
        max_length=10, blank=False, null=False, verbose_name=_("Почтовый индекс (zip)")
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=_("Широта")
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=_("Долгота")
    )

    def __str__(self):
        return f"{self.city}, {self.state} {self.zip_code}"

    class Meta:
        db_table = "service_location"
        verbose_name = _("Локация")
        verbose_name_plural = _("Локации")
