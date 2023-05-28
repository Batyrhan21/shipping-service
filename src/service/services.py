from typing import Union, List
from geopy.distance import geodesic
from geopy.point import Point
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
    ) -> None:
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

    @staticmethod
    def get_nearby_trucks(obj, is_count: bool) -> Union[int, List[str]]:
        pickup_location = obj.pick_up
        pickup_point = Point(pickup_location.latitude, pickup_location.longitude)
        nearby_trucks = models.Truck.objects.filter(is_deleted=False).select_related(
            "curr_location"
        )
        count = 0 if is_count else []
        for truck in nearby_trucks:
            truck_location = truck.curr_location
            truck_point = Point(truck_location.latitude, truck_location.longitude)
            distance = geodesic(pickup_point, truck_point).miles
            if distance <= 450:
                if is_count:
                    count += 1
                count.append(truck.number)
        return count
