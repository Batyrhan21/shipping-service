from geopy.distance import geodesic
from geopy.point import Point
from django.core.validators import MaxValueValidator
from rest_framework import serializers

from service import models


class ShipmentListSerializer(serializers.ModelSerializer):
    pick_up = serializers.PrimaryKeyRelatedField(
        queryset=models.Location.objects.filter(is_deleted=False),
        allow_null=True,
        required=False,
    )
    delivery = serializers.PrimaryKeyRelatedField(
        queryset=models.Location.objects.filter(is_deleted=False),
        allow_null=True,
        required=False,
    )
    count_nearby_trucks = serializers.SerializerMethodField()

    class Meta:
        model = models.Shipment
        fields = [
            "id",
            "pick_up",
            "delivery",
            "weight",
            "description",
            "count_nearby_trucks",
        ]

    def get_count_nearby_trucks(self, obj) -> int:
        pickup_location = obj.pick_up
        pickup_point = Point(pickup_location.latitude, pickup_location.longitude)
        nearby_trucks = models.Truck.objects.filter(is_deleted=False).select_related(
            "curr_location"
        )
        count = 0
        for truck in nearby_trucks:
            truck_location = truck.curr_location
            truck_point = Point(truck_location.latitude, truck_location.longitude)
            distance = geodesic(pickup_point, truck_point).miles
            if distance <= 450:
                count += 1
        return count


class ShipmentCreateSerializer(serializers.ModelSerializer):
    weight = serializers.IntegerField(
        required=True, allow_null=False, validators=[MaxValueValidator(1000)]
    )
    description = serializers.CharField(required=False, allow_null=True)
    pick_up = serializers.CharField(required=True, allow_null=False)
    delivery = serializers.CharField(required=True, allow_null=False)

    class Meta:
        model = models.Shipment
        fields = ["id", "weight", "description", "pick_up", "delivery"]
