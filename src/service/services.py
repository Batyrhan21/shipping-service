import random
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

    @classmethod
    def delete_select_shipments(cls, ids):
        queryset = cls.__shipment_model.objects.filter(id__in=ids)
        queryset.delete()

    @staticmethod
    def get_nearby_trucks(obj, is_count: bool, miles: float) -> Union[int, List[str]]:
        pickup_location = obj.pick_up
        pickup_point = Point(pickup_location.latitude, pickup_location.longitude)
        nearby_trucks = models.Truck.objects.filter(is_deleted=False).select_related(
            "curr_location"
        )
        count = 0
        numbers = []
        for truck in nearby_trucks:
            truck_location = truck.curr_location
            truck_point = Point(truck_location.latitude, truck_location.longitude)
            distance = geodesic(pickup_point, truck_point).miles
            if distance <= float(miles):
                count += 1
                numbers.append({truck.number: f"{distance} miles"})
        if is_count:
            return count
        return numbers


class TruckService:
    __truck_model = models.Truck
    __location_model = models.Location

    @classmethod
    def get_list(cls, **filters) -> QuerySet[models.Truck]:
        return (
            cls.__truck_model.objects.filter(**filters)
            .order_by("-created_at")
            .only("id", "number", "curr_location", "load_capacity")
            .select_related("curr_location")
        )

    @classmethod
    def update_truck_by_zip(cls, instance, location_zip) -> None:
        try:
            qs_location = cls.__location_model.objects.get(zip_code=location_zip)
        except cls.__location_model.DoesNotExist:
            raise ValidationError("Location not found.", code="invalid")
        instance.curr_location = qs_location
        instance.save()


    @classmethod
    def update_location_random(cls) -> None:
        trucks =  cls.__truck_model.objects.filter(is_deleted=False)
        for truck in trucks:
            locations = cls.__location_model.objects.filter(is_deleted=False)
            random_location = random.choice(locations)
            truck.curr_location = random_location
            truck.save()