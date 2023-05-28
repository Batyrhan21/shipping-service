from geopy.distance import geodesic
from geopy.point import Point
from django.core.validators import MaxValueValidator
from rest_framework import serializers

from service import models, services


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
        return services.ShipmentService.get_nearby_trucks(obj=obj,is_count=True)


class ShipmentRetriveSerializer(serializers.ModelSerializer):
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
    number_nearby_trucks = serializers.SerializerMethodField()

    class Meta:
        model = models.Shipment
        fields = [
            "id",
            "pick_up",
            "delivery",
            "weight",
            "description",
            "number_nearby_trucks",
        ]

    def get_number_nearby_trucks(self, obj) -> int:
        return services.ShipmentService.get_nearby_trucks(obj=obj, is_count=False)


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
