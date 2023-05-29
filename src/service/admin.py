from django.contrib import admin
from django.db.models import QuerySet

from service import models


@admin.register(models.Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["pick_up", "delivery", "weight", "description"]
    search_fields = [
        "description",
        "weight",
        "pick_up__city",
        "pick_up__state",
        "pick_up__zip_code",
        "delivery__city",
        "delivery__state",
        "delivery__zip_code",
    ]
    readonly_fields = ["created_at", "id"]
    fields = [
        "pick_up",
        "delivery",
        "weight",
        "description",
        "created_at",
    ]
    raw_id_fields = ["pick_up", "delivery"]

    def get_queryset(self, request) -> QuerySet[models.Shipment]:
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("pick_up", "delivery")
        return queryset


@admin.register(models.Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ["id", "number", "curr_location", "load_capacity"]
    search_fields = ["number", "curr_location__city", "curr_location__state"]
    readonly_fields = ["created_at", "id"]
    fields = [
        "number",
        "load_capacity",
        "created_at",
    ]
    ordering = ["-created_at"]

    def get_queryset(self, request) -> QuerySet[models.Truck]:
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("curr_location")
        return queryset


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["state", "city", "zip_code", "latitude", "longitude"]
    list_filter = ["trucks", "shipment_pickups", "shipment_deliveries"]
    search_fields = ["state", "city", "zip_code", "latitude", "longitude"]
    readonly_fields = ["created_at", "id"]
    fields = ["state", "city", "zip_code", "latitude", "longitude"]
    ordering = ["-created_at"]
