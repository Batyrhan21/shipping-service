from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from service import models


class ShipmentService:
    __shipment_model = models.Shipment
    __location_model = models.Location

    @classmethod
    def get_list(cls, **filters) -> QuerySet[models.Shipment]:
        return (
            cls.__shipment_model.objects.filter(**filters)
            .order_by("-created_at")
            .only("id", "pick_up", "delivery", "weight", "description")
            .select_related("pick_up", "delivery")
        )

    @classmethod
    def create_shipment_by_zip_code(
        cls, pick_zip: str, delivery_zip: str, weight: int, description: str
    ) -> QuerySet[models.Shipment]:
        try:
            pick_location = cls.__location_model.objects.get(zip_code=pick_zip)
            delivery_location = cls.__location_model.objects.get(zip_code=delivery_zip)
        except cls.__location_model.DoesNotExist:
            raise ValidationError("Location not found.", code="invalid")
        return cls.__shipment_model.objects.create(
            pick_up=pick_location,
            delivery=delivery_location,
            weight=weight,
            description=description,
        )
