from django.contrib import admin

from service import models


@admin.register(models.Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["pick_up", "delivery", "weight", "description"]
    list_filter = [
        "delivery",
    ]
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


@admin.register(models.Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ["number", "curr_location", "load_capacity"]
    list_filter = ["curr_location", "load_capacity"]
    search_fields = ["number", "curr_location__city", "curr_location__state"]
    readonly_fields = ["created_at", "id"]
    fields = [
        "number",
        "load_capacity",
        "created_at",
    ]
    ordering = ["-created_at"]


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["state", "city", "zip_code", "latitude", "longitude"]
    list_filter = ["trucks", "shipment_pickups", "shipment_deliveries"]
    search_fields = ["state", "city", "zip_code", "latitude", "longitude"]
    readonly_fields = ["created_at", "id"]
    fields = ["state", "city", "zip_code", "latitude", "longitude"]
    ordering = ["-created_at"]
